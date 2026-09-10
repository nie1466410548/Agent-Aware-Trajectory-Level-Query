# dacomp-005-02：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Profit Margin) | 列：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q12、Q13、Q14、Q15、Q16、Q18、Q19<br>聚合：Q2、Q3、Q4、Q5、Q6、Q7、Q9、Q10、Q12、Q14、Q16、Q19 |
| Q1 / 候选2 | 读取：sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*) | 列：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q12、Q13、Q14、Q15、Q16、Q18、Q19<br>聚合：Q2、Q3、Q4、Q5、Q6、Q7、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q18、Q19 |
| Q2 / 候选1 | 读取：sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Profit Margin)、COUNT(*) | 列：Q3、Q10、Q12、Q18<br>聚合：Q3、Q4、Q5、Q6、Q7、Q9、Q10、Q12、Q14、Q16、Q19 |
| Q2 / 候选2 | 读取：sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin) | 列：Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q12、Q13、Q14、Q15、Q16、Q18、Q19<br>聚合：后续未找到全部所述项同时出现 |
| Q3 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Profit Margin)、AVG(sheet1.Profit)、AVG(sheet1.Total Logistics Revenue)、AVG(sheet1.Total Logistics Cost)、AVG(sheet1.Freight Cost)、AVG(sheet1.Warehousing Cost)、AVG(sheet1.Other Operating Costs)、AVG(sheet1.Sales Quantity)、AVG(sheet1.Discount Amount) | 列：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q3 / 候选2 | 读取：sheet1.Destination<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Destination<br>聚合：COUNT(*) | 列：Q4、Q13、Q15<br>分组：后续未找到全部所述项同时出现<br>聚合：Q4、Q5、Q6、Q7、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q18、Q19 |
| Q3 / 候选3 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q4 / 候选1 | 读取：sheet1.Date<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q9 |
| Q4 / 候选2 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q4 / 候选3 | 读取：sheet1.Consigned Product<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q7、Q14 |
| Q4 / 候选4 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Sales Quantity)、AVG(sheet1.Discount Amount)、AVG(sheet1.List Price Revenue) | 列：Q8<br>聚合：后续未找到全部所述项同时出现 |
| Q5 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q6 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q7 / 候选1 | 读取：sheet1.Date, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q8 / 候选1 | 读取：sheet1.Date, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q9 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10、Q12、Q18 |
| Q9 / 候选2 | 读取：sheet1.Date, sheet1.Profit Margin<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q10 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q18 |
| Q11 / 候选1 | 读取：sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q12 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Sales Quantity le 10（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现<br>过滤：Q16 |
| Q13 / 候选1 | 读取：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q14 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q15 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q16 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Sales Quantity le 10（只描述了部分）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现 |
| Q17 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q18 / 候选1 | 读取：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q19 / 候选1 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q20 / 候选1 | 读取：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q21 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT * FROM sheet1 LIMIT 5
```

### Q2（成功）

```sql
SELECT COUNT(*) AS n_orders, AVG("Profit Margin") AS avg_profit_margin, MIN("Profit Margin") AS min_pm, MAX("Profit Margin") AS max_pm, AVG("Profit") AS avg_profit, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1
```

### Q3（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low_margin' ELSE 'normal' END AS seg, COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_warehouse, AVG("Other Operating Costs") AS avg_other, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount") AS avg_discount, AVG("List Price Revenue") AS avg_list_rev FROM sheet1 GROUP BY seg
```

### Q4（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region, COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, region ORDER BY region, seg
```

### Q5（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Age Range", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Age Range" ORDER BY "Age Range", seg
```

### Q6（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Customer Gender", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Customer Gender" ORDER BY "Customer Gender", seg
```

### Q7（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Consigned Product", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Consigned Product" ORDER BY "Consigned Product", seg
```

### Q8（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, MIN("Sales Quantity") AS min_qty, MAX("Sales Quantity") AS max_qty, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio, AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio, AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit, AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit FROM sheet1 GROUP BY seg
```

### Q9（成功）

```sql
SELECT SUBSTR("Date",1,7) AS ym, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY ym ORDER BY ym
```

### Q10（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio, AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio FROM sheet1 GROUP BY qty_bucket ORDER BY MIN("Sales Quantity")
```

### Q11（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket, COUNT(*) AS n, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_other, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev, AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit, AVG("Discount Amount") AS avg_disc_amt, AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio FROM sheet1 GROUP BY qty_bucket ORDER BY MIN("Sales Quantity")
```

### Q12（成功）

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Sales Quantity") AS avg_qty, AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY disc_bucket ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

### Q13（成功）

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region, COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small, ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc, SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low FROM sheet1 GROUP BY region ORDER BY n_small DESC
```

### Q14（成功）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small, ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Consigned Product" ORDER BY small_pct DESC
```

### Q15（成功）

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small FROM sheet1 GROUP BY province_city HAVING n >= 100 ORDER BY low_pct DESC LIMIT 15
```

### Q16（成功）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Age Range", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio, AVG("Logistics Unit Price") AS avg_unit_price FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY seg, "Age Range" ORDER BY "Age Range", seg
```

### Q17（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg, SUM("Profit") AS total_profit, SUM("Total Logistics Revenue") AS total_rev, SUM("Total Logistics Cost") AS total_cost, SUM("Freight Cost") AS total_freight, SUM("Warehousing Cost") AS total_wh, SUM("Other Operating Costs") AS total_other, SUM("Discount Amount") AS total_discount FROM sheet1 GROUP BY size_seg
```

### Q18（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg, COUNT(*) AS n, SUM("Profit") AS total_profit, SUM("Total Logistics Revenue") AS total_rev, SUM("Total Logistics Cost") AS total_cost, SUM("Discount Amount") AS total_disc, SUM("Freight Cost") AS total_freight, SUM("Warehousing Cost") AS total_wh, SUM("Other Operating Costs") AS total_other, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio FROM sheet1 GROUP BY seg
```

### Q19（成功）

```sql
SELECT "Sales Quantity" AS qty, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio FROM sheet1 GROUP BY qty HAVING qty <= 10 ORDER BY qty
```

### Q20（成功）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg, AVG("Logistics Value-Added Service Revenue") AS avg_vas, SUM("Logistics Value-Added Service Revenue") AS total_vas, AVG("Logistics Unit Price") AS avg_unit_price, AVG("List Price Revenue") AS avg_list_rev, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1 GROUP BY size_seg
```

### Q21（成功）

```sql
SELECT 1
```
