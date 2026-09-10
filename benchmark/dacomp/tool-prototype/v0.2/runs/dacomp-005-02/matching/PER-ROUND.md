# dacomp-005：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q1 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | Q2, Q3, Q4, Q5, Q6, Q7, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q18, Q19 | 没有提供具体项（none） |
| Q2 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"Profit Margin","function":"avg"},{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q2 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"Profit Margin","function":"min"},{"column":"Profit Margin","function":"max"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q3 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Logistics Unit Price"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"Profit Margin","function":"avg"},{"column":"Profit","function":"avg"},{"column":"Total Logistics Revenue","function":"avg"},{"column":"Total Logistics Cost","function":"avg"},{"column":"Freight Cost","function":"avg"},{"column":"Warehousing Cost","function":"avg"},{"column":"Other Operating Costs","function":"avg"},{"column":"Sales Quantity","function":"avg"},{"column":"Discount Amount","function":"avg"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q3 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Destination"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q4, Q5, Q6, Q7, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q18, Q19 | 没有提供具体项（none） |
| Q3 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Age Range","sheet1.Customer Gender","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: low | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q4 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q4 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q4 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q4 / 4 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Quantity","sheet1.Logistics Unit Price","sheet1.List Price Revenue","sheet1.Discount Amount","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"Sales Quantity","function":"avg"},{"column":"Discount Amount","function":"avg"},{"column":"List Price Revenue","function":"avg"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q5 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Age Range","sheet1.Customer Gender","sheet1.Consigned Product","sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Profit"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q6 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer Gender","sheet1.Consigned Product","sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q7 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q8 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Logistics Unit Price","sheet1.Discount Amount","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q9 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Profit"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q9 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q10 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q11 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Destination"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q12 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Consigned Product","sheet1.Destination","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Sales Quantity","op":"le","type":"predicate","value":{"literal":10,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q16 |
| Q13 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Destination","sheet1.Consigned Product","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q14 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Destination","sheet1.Consigned Product","sheet1.Logistics Unit Price","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q15 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Destination","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q16 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Sales Quantity","op":"le","type":"predicate","value":{"literal":10,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 未发现对应查询 |
| Q17 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.List Price Revenue","sheet1.Logistics Unit Price"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q18 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Logistics Value-Added Service Revenue","sheet1.Logistics Unit Price"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q19 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Logistics Value-Added Service Revenue","sheet1.Logistics Unit Price","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q20 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Logistics Value-Added Service Revenue","sheet1.Logistics Unit Price","sheet1.List Price Revenue","sheet1.Logistics Unit Price"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: low | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q21 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT * FROM sheet1 LIMIT 5
```

### Q2（ok）

```sql
SELECT COUNT(*) AS n_orders, AVG("Profit Margin") AS avg_profit_margin, MIN("Profit Margin") AS min_pm, MAX("Profit Margin") AS max_pm, AVG("Profit") AS avg_profit, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1
```

### Q3（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low_margin' ELSE 'normal' END AS seg, COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_warehouse, AVG("Other Operating Costs") AS avg_other, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount") AS avg_discount, AVG("List Price Revenue") AS avg_list_rev FROM sheet1 GROUP BY seg
```

### Q4（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region, COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, region ORDER BY region, seg
```

### Q5（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Age Range", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Age Range" ORDER BY "Age Range", seg
```

### Q6（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Customer Gender", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Customer Gender" ORDER BY "Customer Gender", seg
```

### Q7（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Consigned Product", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, SUM("Profit") AS total_profit FROM sheet1 GROUP BY seg, "Consigned Product" ORDER BY "Consigned Product", seg
```

### Q8（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, MIN("Sales Quantity") AS min_qty, MAX("Sales Quantity") AS max_qty, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio, AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio, AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit, AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit FROM sheet1 GROUP BY seg
```

### Q9（ok）

```sql
SELECT SUBSTR("Date",1,7) AS ym, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY ym ORDER BY ym
```

### Q10（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio, AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio FROM sheet1 GROUP BY qty_bucket ORDER BY MIN("Sales Quantity")
```

### Q11（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket, COUNT(*) AS n, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_other, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev, AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit, AVG("Discount Amount") AS avg_disc_amt, AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio FROM sheet1 GROUP BY qty_bucket ORDER BY MIN("Sales Quantity")
```

### Q12（ok）

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Sales Quantity") AS avg_qty, AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY disc_bucket ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

### Q13（ok）

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region, COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small, ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc, SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low FROM sheet1 GROUP BY region ORDER BY n_small DESC
```

### Q14（ok）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small, ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Consigned Product" ORDER BY small_pct DESC
```

### Q15（ok）

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small FROM sheet1 GROUP BY province_city HAVING n >= 100 ORDER BY low_pct DESC LIMIT 15
```

### Q16（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg, "Age Range", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio, AVG("Logistics Unit Price") AS avg_unit_price FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY seg, "Age Range" ORDER BY "Age Range", seg
```

### Q17（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg, SUM("Profit") AS total_profit, SUM("Total Logistics Revenue") AS total_rev, SUM("Total Logistics Cost") AS total_cost, SUM("Freight Cost") AS total_freight, SUM("Warehousing Cost") AS total_wh, SUM("Other Operating Costs") AS total_other, SUM("Discount Amount") AS total_discount FROM sheet1 GROUP BY size_seg
```

### Q18（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg, COUNT(*) AS n, SUM("Profit") AS total_profit, SUM("Total Logistics Revenue") AS total_rev, SUM("Total Logistics Cost") AS total_cost, SUM("Discount Amount") AS total_disc, SUM("Freight Cost") AS total_freight, SUM("Warehousing Cost") AS total_wh, SUM("Other Operating Costs") AS total_other, AVG("Sales Quantity") AS avg_qty, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio FROM sheet1 GROUP BY seg
```

### Q19（ok）

```sql
SELECT "Sales Quantity" AS qty, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low, ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio FROM sheet1 GROUP BY qty HAVING qty <= 10 ORDER BY qty
```

### Q20（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg, AVG("Logistics Value-Added Service Revenue") AS avg_vas, SUM("Logistics Value-Added Service Revenue") AS total_vas, AVG("Logistics Unit Price") AS avg_unit_price, AVG("List Price Revenue") AS avg_list_rev, AVG("Total Logistics Revenue") AS avg_rev FROM sheet1 GROUP BY size_seg
```

### Q21（ok）

```sql
SELECT 1
```
