# dacomp-005-01：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q1 / 候选2 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 值尚未确定（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q2 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 值尚未确定（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q2 / 候选2 | 读取：sheet1.Destination, sheet1.Profit Margin<br>过滤：sheet1.Profit Margin lt 值尚未确定（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Destination<br>聚合：COUNT(*)、AVG(sheet1.Profit Margin) | 列：Q4、Q5、Q19<br>分组：Q4、Q19<br>聚合：Q3、Q4、Q5、Q6、Q7、Q11、Q12、Q14、Q15、Q16、Q17、Q27 |
| Q3 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Sales Quantity)、AVG(sheet1.Total Logistics Revenue)、AVG(sheet1.Discount Amount)、AVG(sheet1.Freight Cost)、AVG(sheet1.Warehousing Cost)、AVG(sheet1.Other Operating Costs)、AVG(sheet1.Total Logistics Cost)、AVG(sheet1.Profit) | 列：后续未找到全部所述项同时出现<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24<br>聚合：Q27 |
| Q3 / 候选2 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin ge 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Sales Quantity)、AVG(sheet1.Total Logistics Revenue)、AVG(sheet1.Discount Amount)、AVG(sheet1.Freight Cost)、AVG(sheet1.Warehousing Cost)、AVG(sheet1.Other Operating Costs)、AVG(sheet1.Total Logistics Cost)、AVG(sheet1.Profit) | 列：后续未找到全部所述项同时出现<br>过滤：Q25<br>聚合：Q27 |
| Q4 / 候选1 | 读取：sheet1.Destination, sheet1.Profit Margin<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Destination<br>聚合：COUNT(*)、AVG(sheet1.Profit Margin) | 列：Q5、Q19<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24<br>分组：Q19<br>聚合：Q5、Q6、Q7、Q11、Q12、Q14、Q15、Q16、Q17、Q27 |
| Q4 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Profit Margin<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Consigned Product<br>聚合：COUNT(*)、AVG(sheet1.Profit Margin) | 列：Q6、Q18<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24<br>分组：Q6、Q18<br>聚合：Q5、Q6、Q7、Q11、Q12、Q14、Q15、Q16、Q17、Q27 |
| Q4 / 候选3 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q5 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Profit Margin<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Consigned Product<br>聚合：COUNT(*)、AVG(sheet1.Profit Margin) | 列：Q6、Q18<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24<br>分组：Q6、Q18<br>聚合：Q6、Q7、Q11、Q12、Q14、Q15、Q16、Q17、Q27 |
| Q5 / 候选2 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q5 / 候选3 | 读取：sheet1.Destination, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q19 |
| Q6 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q6 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q9、Q10 |
| Q7 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q7 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q9、Q10 |
| Q7 / 候选3 | 读取：sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q8、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q23、Q24、Q27、Q28 |
| Q8 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q8 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q9、Q10 |
| Q8 / 候选3 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q14、Q17、Q22、Q23、Q24<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24 |
| Q9 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q9 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10 |
| Q9 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q18 |
| Q10 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q10 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q18 |
| Q11 / 候选1 | 读取：sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Customer Gender<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>分组：Q12<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q28 |
| Q11 / 候选2 | 读取：sheet1.Age Range, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q11 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q18 |
| Q12 / 候选1 | 读取：sheet1.Customer Age, sheet1.Customer Gender, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q12 / 候选2 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现<br>过滤：Q13、Q14、Q15、Q16、Q17、Q24 |
| Q13 / 候选1 | 读取：sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*) | 列：Q14、Q15、Q16、Q17、Q21、Q22、Q24、Q27<br>过滤：Q14、Q15、Q16、Q17、Q24<br>聚合：Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q28 |
| Q13 / 候选2 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q14、Q17、Q22、Q23、Q24<br>过滤：Q14、Q15、Q16、Q17、Q24 |
| Q14 / 候选1 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q23、Q24<br>过滤：Q15、Q16、Q17、Q24 |
| Q14 / 候选2 | 读取：sheet1.Destination, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q19<br>过滤：Q15、Q16、Q17、Q24 |
| Q15 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q24<br>过滤：Q16、Q17、Q24 |
| Q16 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q24<br>过滤：Q17、Q24 |
| Q17 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Profit Margin lt 0.3976（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q22、Q24<br>过滤：Q24 |
| Q18 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：sheet1.Sales Quantity le 10（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现<br>过滤：Q23 |
| Q19 / 候选1 | 读取：sheet1.Destination, sheet1.Freight Cost, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q19 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q20 / 候选1 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q23、Q24 |
| Q21 / 候选1 | 读取：sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q22、Q24、Q27 |
| Q22 | 没有候选：no_further_access | — |
| Q23 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Sales Quantity le 10（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q24<br>过滤：后续未找到全部所述项同时出现 |
| Q24 | 没有候选：no_further_access | — |
| Q25 | 没有候选：no_further_access | — |
| Q26 | 没有候选：no_further_access | — |
| Q27 | 没有候选：no_further_access | — |
| Q28 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT * FROM sheet1 LIMIT 10
```

### Q2（成功）

```sql
SELECT COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, MIN("Profit Margin") AS min_pm, MAX("Profit Margin") AS max_pm FROM sheet1
```

### Q3（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low_margin' ELSE 'normal' END AS grp, COUNT(*) AS n, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Discount Amount") AS avg_disc, AVG("List Price Revenue") AS avg_list, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY grp
```

### Q4（成功）

```sql
SELECT "Destination", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY "Destination" ORDER BY low_cnt DESC LIMIT 20
```

### Q5（成功）

```sql
SELECT substr("Destination", 1, instr("Destination", '-') - 1) AS region, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY region ORDER BY low_cnt DESC
```

### Q6（成功）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 GROUP BY "Consigned Product" ORDER BY low_cnt DESC
```

### Q7（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```

### Q8（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' ELSE 'qty_>10' END AS band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, AVG("Discount Amount") AS avg_disc, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Freight Cost" / NULLIF("Total Logistics Revenue", 0)) AS freight_share_rev, AVG("Warehousing Cost" / NULLIF("Total Logistics Revenue", 0)) AS wh_share_rev, AVG("Other Operating Costs" / NULLIF("Total Logistics Revenue", 0)) AS ooc_share_rev, AVG("Total Logistics Cost" / NULLIF("Total Logistics Revenue", 0)) AS cost_share_rev FROM sheet1 GROUP BY band
```

### Q9（成功）

```sql
SELECT strftime('%Y', "Date") AS year, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY year ORDER BY year
```

### Q10（成功）

```sql
SELECT strftime('%Y-%m', "Date") AS month, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY month ORDER BY month
```

### Q11（成功）

```sql
SELECT "Age Range", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Age Range" ORDER BY low_pct DESC
```

### Q12（成功）

```sql
SELECT "Customer Gender", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Customer Gender"
```

### Q13（成功）

```sql
SELECT SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit_cnt, SUM(CASE WHEN "Profit Margin" < 0 THEN 1 ELSE 0 END) AS neg_pm_cnt, COUNT(*) AS n, AVG("Sales Quantity") AS avg_qty, MIN("Sales Quantity") AS min_qty, MAX("Sales Quantity") AS max_qty FROM sheet1 WHERE "Profit Margin" < 0.3976
```

### Q14（成功）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Discount Amount") AS avg_disc, AVG("List Price Revenue") AS avg_list FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q15（成功）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 AND "Sales Quantity" >= 13 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q16（成功）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 AND "Sales Quantity" >= 25 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q17（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'low_qty' ELSE 'high_qty' END AS qty_group, COUNT(*) AS n, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Freight Cost" / NULLIF("Total Logistics Revenue", 0)) AS freight_pct, AVG("Warehousing Cost" / NULLIF("Total Logistics Revenue", 0)) AS wh_pct, AVG("Other Operating Costs" / NULLIF("Total Logistics Revenue", 0)) AS ooc_pct, AVG(("Freight Cost" + "Warehousing Cost" + "Other Operating Costs") / NULLIF("Total Logistics Revenue", 0)) AS total_cost_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Logistics Value-Added Service Revenue" / NULLIF("Total Logistics Revenue", 0)) AS vas_pct_rev FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY qty_group
```

### Q18（成功）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS small_cnt, ROUND(100.0 * SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) / COUNT(*), 2) AS small_pct, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt FROM sheet1 GROUP BY "Consigned Product" ORDER BY small_pct DESC
```

### Q19（成功）

```sql
SELECT "Destination", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Freight Cost") AS avg_freight FROM sheet1 GROUP BY "Destination" HAVING COUNT(*) >= 100 ORDER BY low_pct DESC LIMIT 15
```

### Q20（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, AVG("Discount Amount") AS avg_disc_abs, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Logistics Unit Price") AS avg_unit_price, AVG("List Price Revenue" / NULLIF("Sales Quantity", 0)) AS avg_list_per_unit FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```

### Q21（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, SUM("Profit") AS tot_profit, SUM("Total Logistics Revenue") AS tot_rev, SUM("Total Logistics Cost") AS tot_cost, SUM("Sales Quantity") AS tot_qty, ROUND(AVG("Profit"), 2) AS avg_profit FROM sheet1 GROUP BY grp
```

### Q22（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, SUM("Discount Amount") AS tot_disc, SUM("List Price Revenue") AS tot_list, SUM("Logistics Value-Added Service Revenue") AS tot_vas, SUM("Freight Cost") AS tot_freight, SUM("Warehousing Cost") AS tot_wh, SUM("Other Operating Costs") AS tot_ooc, SUM("Total Logistics Cost") AS tot_cost, SUM("Total Logistics Revenue") AS tot_rev, SUM("Profit") AS tot_profit, SUM("Sales Quantity") AS tot_qty, COUNT(*) AS n FROM sheet1 GROUP BY grp
```

### Q23（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, AVG("Logistics Unit Price") AS avg_unit, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev, AVG("Logistics Value-Added Service Revenue") AS avg_vas FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY grp
```

### Q24（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS sz, COUNT(*) AS n, AVG("Logistics Unit Price") AS avg_unit, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY sz
```

### Q25（成功）

```sql
SELECT COUNT(*) AS n_between FROM sheet1 WHERE "Profit Margin" >= 0.3976 AND "Profit Margin" < 0.3976434082191792
```

### Q26（成功）

```sql
SELECT COUNT(*) AS low_cnt_exact, SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit FROM sheet1 WHERE "Profit Margin" < 0.7952868164383584 * 0.5
```

### Q27（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, SUM("Profit") AS tot_profit, SUM("Total Logistics Revenue") AS tot_rev, SUM("Total Logistics Cost") AS tot_cost, SUM("Sales Quantity") AS tot_qty, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm, AVG("Discount Amount") AS avg_disc, AVG("Logistics Unit Price") AS avg_unit, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Logistics Value-Added Service Revenue") AS avg_vas FROM sheet1 GROUP BY grp
```

### Q28（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```
