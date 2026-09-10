# dacomp-004：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q3, Q4, Q5, Q9 | Q3, Q4, Q5, Q9, Q10 | 没有提供具体项（none） |
| Q2 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q3, Q4, Q5, Q9 | Q3, Q4, Q5, Q9, Q10 | 没有提供具体项（none） |
| Q3 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Sales Month","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: high | Q4, Q5, Q9 | Q4, Q5, Q9, Q10 | 没有提供具体项（none） |
| Q4 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Sales Month","sheet1.Product Code","sheet1.Sales Amount","sheet1.Customer ID","sheet1.Is Promotional","sheet1.Product Type","sheet1.Major Category Name","sheet1.Middle Category Name","sheet1.Minor Category Name","sheet1.Specification/Model"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q5 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Sales Month","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Product Code","op":"in","type":"predicate","value":{"literal":["DW-1001040125","DW-2316020016","DW-1203130446","DW-1518040045"],"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Customer ID","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Month","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7 | Q7, Q10 | Q6, Q7, Q8, Q9, Q10 |
| Q6 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Sales Month","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Product Code","op":"in","type":"predicate","value":{"literal":["DW-1001040125","DW-2316020016","DW-1203130446","DW-1518040045"],"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Customer ID","type":"column"},{"column":"sheet1.Product Code","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Sales Month","function":"count_distinct"}],"status":"known"}<br>priority: high | Q7 | Q7, Q10 | Q7, Q8, Q9, Q10 |
| Q7 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Sales Month","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Product Code","op":"in","type":"predicate","value":{"literal":["DW-1001040125","DW-2316020016","DW-1203130446","DW-1518040045"],"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | Q8, Q9, Q10 |
| Q8 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Customer ID","sheet1.Sales Month","sheet1.Product Code"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Product Code","op":"in","type":"predicate","value":{"literal":["DW-1001040125","DW-2316020016","DW-1203130446","DW-1518040045"],"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | Q9, Q10 |
| Q9 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Product Code","sheet1.Sales Amount"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Product Code","op":"in","type":"predicate","value":{"literal":["DW-1001040125","DW-2316020016","DW-1203130446","DW-1518040045"],"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"sheet1.Sales Amount","function":"sum"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | Q10 | Q10 |
| Q10 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT * FROM sheet1 LIMIT 20
```

### Q2（ok）

```sql
SELECT COUNT(*) AS row_count, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Sales Month") AS n_months, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month FROM sheet1
```

### Q3（ok）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales
FROM sheet1
GROUP BY "Sales Month", "Product Code"
ORDER BY "Sales Month", total_sales DESC
```

### Q4（ok）

```sql
SELECT * FROM (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month" ORDER BY SUM("Sales Amount") DESC) AS rnk
  FROM sheet1
  GROUP BY "Sales Month", "Product Code"
) WHERE rnk = 1
ORDER BY "Sales Month"
```

### Q5（ok）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions, COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"
```

### Q6（ok）

```sql
SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit"
```

### Q7（ok）

```sql
SELECT "Product Code",
       COUNT(DISTINCT "Customer ID") AS total_customers,
       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
  SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
  FROM sheet1
  WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
  GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

### Q8（ok）

```sql
SELECT "Product Code",
       COUNT(*) AS total_rows,
       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
  SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID" ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
  FROM sheet1
  WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

### Q9（ok）

```sql
SELECT * FROM (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month" ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
  FROM sheet1
  GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code", "Sales Month"
```

### Q10（ok）

```sql
SELECT "Product Code", SUM("Sales Amount") AS total_sales,
       COUNT(DISTINCT "Customer ID") AS total_customers,
       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```
