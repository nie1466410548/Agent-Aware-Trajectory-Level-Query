# dacomp-004-01：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q4、Q5、Q6、Q7、Q11、Q12、Q13、Q14<br>分组：Q4、Q5、Q6、Q11、Q12、Q13、Q14<br>聚合：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14 |
| Q1 / 候选2 | 读取：sheet1., sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code（只描述了部分）<br>聚合：SUM(sheet1.Sales Amount)、COUNT(sheet1.Customer ID)（只描述了部分） | 列：后续未找到全部所述项同时出现<br>分组：Q4、Q5、Q6、Q11、Q12、Q13、Q14<br>聚合：后续未找到全部所述项同时出现 |
| Q2 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q4、Q5、Q6、Q7、Q11、Q12、Q13、Q14<br>分组：Q4、Q5、Q6、Q11、Q12、Q13、Q14<br>聚合：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14 |
| Q2 / 候选2 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Customer ID) | 列：Q4、Q6、Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q4、Q6 |
| Q3 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q4、Q5、Q6、Q7、Q11、Q12、Q13、Q14<br>分组：Q4、Q5、Q6、Q11、Q12、Q13、Q14<br>聚合：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14 |
| Q3 / 候选2 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Customer ID) | 列：Q4、Q6、Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q4、Q6 |
| Q4 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Customer ID) | 列：Q6、Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q6 |
| Q4 / 候选2 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q5、Q6、Q7、Q11、Q12、Q13、Q14<br>分组：Q5、Q6、Q11、Q12、Q13、Q14<br>聚合：Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14 |
| Q4 / 候选3 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT(sheet1.Customer ID) | 列：Q6、Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：后续未找到全部所述项同时出现 |
| Q5 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q6、Q7、Q11、Q12、Q13、Q14<br>分组：Q6、Q11、Q12、Q13、Q14<br>聚合：Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14 |
| Q5 / 候选2 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Customer ID) | 列：Q6、Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q6 |
| Q6 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：Q7、Q8、Q9<br>分组：Q7、Q8、Q9<br>聚合：后续未找到全部所述项同时出现 |
| Q6 / 候选2 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Customer ID) | 列：Q7、Q8、Q9<br>分组：Q7、Q8、Q9、Q10<br>聚合：后续未找到全部所述项同时出现 |
| Q7 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Amount<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount)、COUNT_DISTINCT(sheet1.Customer ID) | 列：Q8、Q9<br>分组：Q8、Q9、Q10<br>聚合：后续未找到全部所述项同时出现 |
| Q7 / 候选2 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Amount<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount)、COUNT_DISTINCT(sheet1.Customer ID)、COUNT(sheet1.Customer ID) | 列：Q8、Q9<br>分组：Q8、Q9、Q10<br>聚合：后续未找到全部所述项同时出现 |
| Q8 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：Q9<br>分组：Q9<br>聚合：后续未找到全部所述项同时出现 |
| Q9 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q10 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q11 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q12 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Product Code ＋ sheet1.Customer ID<br>聚合：COUNT(sheet1.Customer ID) | 列：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q13 | 没有候选：no_further_access | — |
| Q14 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT * FROM sheet1 LIMIT 20
```

### Q2（成功）

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Sales Month") AS n_months, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Customer ID") AS n_customers, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month FROM sheet1
```

### Q3（成功）

```sql
SELECT DISTINCT "Sales Month" FROM sheet1 ORDER BY "Sales Month"
```

### Q4（成功）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales, COUNT(*) AS n_orders, COUNT(DISTINCT "Customer ID") AS n_customers FROM sheet1 GROUP BY "Sales Month", "Product Code" ORDER BY "Sales Month", month_sales DESC
```

### Q5（成功）

```sql
WITH monthly AS (SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales FROM sheet1 GROUP BY "Sales Month", "Product Code"), ranked AS (SELECT "Sales Month", "Product Code", month_sales, ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY month_sales DESC, "Product Code") AS rn FROM monthly) SELECT "Sales Month", "Product Code", month_sales FROM ranked WHERE rn = 1 ORDER BY "Sales Month"
```

### Q6（成功）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS month_sales, COUNT(*) AS n_orders, COUNT(DISTINCT "Customer ID") AS n_customers FROM sheet1 WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045') GROUP BY "Sales Month", "Product Code" ORDER BY "Product Code", "Sales Month"
```

### Q7（成功）

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

### Q8（成功）

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

### Q9（成功）

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

### Q10（成功）

```sql
SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", "Is Promotional", COUNT(*) AS n_records, SUM("Sales Amount") AS total_sales FROM sheet1 WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045') GROUP BY "Product Code"
```

### Q11（成功）

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

### Q12（成功）

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

### Q13（成功）

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

### Q14（成功）

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
