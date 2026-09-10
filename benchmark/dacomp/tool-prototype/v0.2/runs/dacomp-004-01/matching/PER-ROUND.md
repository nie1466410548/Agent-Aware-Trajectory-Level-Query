# dacomp-004：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q4, Q5, Q6, Q11, Q12, Q13, Q14 | Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14 | 没有提供具体项（none） |
| Q1 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount","sheet1."],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"partial"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"},{"column":"sheet1.Customer ID","function":"count"}],"status":"partial"}<br>priority: high | Q4, Q5, Q6, Q11, Q12, Q13, Q14 | 未发现对应查询 | 没有提供具体项（none） |
| Q2 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q4, Q5, Q6, Q11, Q12, Q13, Q14 | Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14 | 没有提供具体项（none） |
| Q2 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7, Q8, Q9, Q10 | Q4, Q6 | 没有提供具体项（none） |
| Q3 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q4, Q5, Q6, Q11, Q12, Q13, Q14 | Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14 | 没有提供具体项（none） |
| Q3 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7, Q8, Q9, Q10 | Q4, Q6 | 没有提供具体项（none） |
| Q4 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7, Q8, Q9, Q10 | Q6 | 没有提供具体项（none） |
| Q4 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q5, Q6, Q11, Q12, Q13, Q14 | Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14 | 没有提供具体项（none） |
| Q4 / 3 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | Q7, Q8, Q9, Q10 | 未发现对应查询 | 没有提供具体项（none） |
| Q5 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q6, Q11, Q12, Q13, Q14 | Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14 | 没有提供具体项（none） |
| Q5 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7, Q8, Q9, Q10 | Q6 | 没有提供具体项（none） |
| Q6 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | Q7, Q8, Q9 | 未发现对应查询 | 没有提供具体项（none） |
| Q6 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7, Q8, Q9, Q10 | 未发现对应查询 | 没有提供具体项（none） |
| Q7 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Sales Amount","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"},{"column":"sheet1.Customer ID","function":"count_distinct"}],"status":"known"}<br>priority: high | Q8, Q9, Q10 | 未发现对应查询 | 没有提供具体项（none） |
| Q7 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"},{"column":"sheet1.Customer ID","function":"count_distinct"},{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: high | Q8, Q9, Q10 | 未发现对应查询 | 没有提供具体项（none） |
| Q8 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | Q9 | 未发现对应查询 | 没有提供具体项（none） |
| Q9 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Customer ID"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q10 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q11 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q12 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Product Code","type":"column"},{"column":"sheet1.Customer ID","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Customer ID","function":"count"}],"status":"known"}<br>priority: medium | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q13 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q14 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT * FROM sheet1 LIMIT 20
```

### Q2（ok）

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Sales Month") AS n_months, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Customer ID") AS n_customers, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month FROM sheet1
```

### Q3（ok）

```sql
SELECT DISTINCT "Sales Month" FROM sheet1 ORDER BY "Sales Month"
```

### Q4（ok）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales, COUNT(*) AS n_orders, COUNT(DISTINCT "Customer ID") AS n_customers FROM sheet1 GROUP BY "Sales Month", "Product Code" ORDER BY "Sales Month", month_sales DESC
```

### Q5（ok）

```sql
WITH monthly AS (SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales FROM sheet1 GROUP BY "Sales Month", "Product Code"), ranked AS (SELECT "Sales Month", "Product Code", month_sales, ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC, "Product Code") AS rn FROM monthly) SELECT "Sales Month", "Product Code", month_sales FROM ranked WHERE rn = 1 ORDER BY "Sales Month"
```

### Q6（ok）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales, COUNT(*) AS n_orders, COUNT(DISTINCT "Customer ID") AS n_customers FROM sheet1 WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045') GROUP BY "Sales Month", "Product Code" ORDER BY "Product Code", "Sales Month"
```

### Q7（ok）

```sql
WITH cust_prod AS (
  SELECT "Product Code", "Customer ID",
         COUNT(*) AS n_purchases,
         COUNT(DISTINCT "Sales Month") AS n_months,
         SUM("Sales Amount") AS cust_amount
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
)
SELECT "Product Code",
       COUNT(*) AS n_customers,
       SUM(CASE WHEN n_purchases >= 2 THEN 1 ELSE 0 END) AS n_repurchasers,
       ROUND(100.0 * SUM(CASE WHEN n_purchases >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repurchase_rate_pct,
       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS n_multi_month,
       ROUND(100.0 * SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS multi_month_rate_pct,
       ROUND(SUM(cust_amount), 2) AS total_sales,
       SUM(n_purchases) AS n_orders
FROM cust_prod
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

### Q8（ok）

```sql
WITH cust_prod AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS n_purchases, SUM("Sales Amount") AS cust_amount
  FROM sheet1 GROUP BY "Product Code", "Customer ID"
), prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN n_purchases >= 2 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS repurchase_rate,
         SUM(cust_amount) AS total_sales
  FROM cust_prod GROUP BY "Product Code"
)
SELECT CASE
         WHEN total_sales < 100 THEN '1: <100'
         WHEN total_sales < 500 THEN '2: 100-500'
         WHEN total_sales < 1000 THEN '3: 500-1000'
         WHEN total_sales < 2000 THEN '4: 1000-2000'
         WHEN total_sales < 5000 THEN '5: 2000-5000'
         ELSE '6: >=5000'
       END AS sales_bucket,
       COUNT(*) AS n_products,
       ROUND(AVG(repurchase_rate) * 100, 2) AS avg_repurchase_rate_pct,
       ROUND(MIN(repurchase_rate) * 100, 2) AS min_rate_pct,
       ROUND(MAX(repurchase_rate) * 100, 2) AS max_rate_pct,
       ROUND(AVG(total_sales), 2) AS avg_sales,
       ROUND(AVG(n_customers), 1) AS avg_customers
FROM prod_stats
GROUP BY sales_bucket
ORDER BY sales_bucket
```

### Q9（ok）

```sql
WITH cust_prod AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS n_purchases, SUM("Sales Amount") AS cust_amount
  FROM sheet1 GROUP BY "Product Code", "Customer ID"
), prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN n_purchases >= 2 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS repurchase_rate,
         SUM(cust_amount) AS total_sales
  FROM cust_prod GROUP BY "Product Code"
)
SELECT COUNT(*) AS n,
       ROUND((COUNT(*) * SUM(total_sales * repurchase_rate) - SUM(total_sales) * SUM(repurchase_rate)) /
         SQRT((COUNT(*) * SUM(total_sales * total_sales) - SUM(total_sales) * SUM(total_sales)) *
              (COUNT(*) * SUM(repurchase_rate * repurchase_rate) - SUM(repurchase_rate) * SUM(repurchase_rate))), 4) AS pearson_r_sales_vs_rate
FROM prod_stats
```

### Q10（ok）

```sql
SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", "Is Promotional", COUNT(*) AS n_records, SUM("Sales Amount") AS total_sales FROM sheet1 WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045') GROUP BY "Product Code"
```

### Q11（ok）

```sql
WITH monthly AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales
  FROM sheet1 GROUP BY "Sales Month", "Product Code"
), ranked AS (
  SELECT "Sales Month", "Product Code", month_sales,
         RANK() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC) AS rk,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
  FROM monthly
)
SELECT "Sales Month", "Product Code", ROUND(month_sales, 2) AS month_sales, rk, n_products_in_month
FROM ranked
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
ORDER BY "Sales Month", rk
```

### Q12（ok）

```sql
WITH monthly AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales
  FROM sheet1 GROUP BY "Sales Month", "Product Code"
), ranked AS (
  SELECT "Sales Month", "Product Code", month_sales,
         ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC, "Product Code") AS rn
  FROM monthly
)
SELECT "Sales Month", "Product Code", ROUND(month_sales, 2) AS month_sales, rn
FROM ranked
WHERE rn <= 5
ORDER BY "Sales Month", rn
```

### Q13（ok）

```sql
WITH monthly AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales
  FROM sheet1 GROUP BY "Sales Month", "Product Code"
), ranked AS (
  SELECT "Sales Month", "Product Code", month_sales,
         ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC, "Product Code") AS rn
  FROM monthly
)
SELECT "Sales Month", "Product Code", ROUND(month_sales, 2) AS month_sales, rn
FROM ranked
WHERE rn <= 5
ORDER BY "Sales Month", rn
```

### Q14（ok）

```sql
WITH monthly AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales
  FROM sheet1 GROUP BY "Sales Month", "Product Code"
), ranked AS (
  SELECT "Sales Month", "Product Code", month_sales,
         ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC, "Product Code") AS rn
  FROM monthly
)
SELECT "Sales Month", "Product Code", ROUND(month_sales, 2) AS month_sales, rn
FROM ranked
WHERE rn <= 5 AND "Sales Month" >= 201503
ORDER BY "Sales Month", rn
```
