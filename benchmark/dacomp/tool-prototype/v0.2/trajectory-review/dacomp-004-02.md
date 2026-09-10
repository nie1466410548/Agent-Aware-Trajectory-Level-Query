# dacomp-004-02：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q3、Q4、Q5、Q9、Q10<br>分组：Q3、Q4、Q5、Q9<br>聚合：Q3、Q4、Q5、Q9、Q10 |
| Q2 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q3、Q4、Q5、Q9、Q10<br>分组：Q3、Q4、Q5、Q9<br>聚合：Q3、Q4、Q5、Q9、Q10 |
| Q3 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Sales Month ＋ sheet1.Product Code<br>聚合：SUM(sheet1.Sales Amount) | 列：Q4、Q5、Q9、Q10<br>分组：Q4、Q5、Q9<br>聚合：Q4、Q5、Q9、Q10 |
| Q4 / 候选1 | 读取：sheet1.Customer ID, sheet1.Is Promotional, sheet1.Major Category Name, sheet1.Middle Category Name, sheet1.Minor Category Name, sheet1.Product Code, sheet1.Product Type, sheet1.Sales Amount, sheet1.Sales Month, sheet1.Specification/Model<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：后续未找到全部所述项同时出现 |
| Q5 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month<br>过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]<br>连接：未提供（none）<br>分组：sheet1.Customer ID ＋ sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Sales Month) | 列：Q7、Q8、Q10<br>过滤：Q6、Q7、Q8、Q9、Q10<br>分组：Q7<br>聚合：Q7、Q10 |
| Q6 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month<br>过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]<br>连接：未提供（none）<br>分组：sheet1.Customer ID ＋ sheet1.Product Code<br>聚合：COUNT_DISTINCT(sheet1.Sales Month) | 列：Q7、Q8、Q10<br>过滤：Q7、Q8、Q9、Q10<br>分组：Q7<br>聚合：Q7、Q10 |
| Q7 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month<br>过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q8、Q10<br>过滤：Q8、Q9、Q10 |
| Q8 / 候选1 | 读取：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month<br>过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10<br>过滤：Q9、Q10 |
| Q9 / 候选1 | 读取：sheet1.Product Code, sheet1.Sales Amount<br>过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：SUM(sheet1.Sales Amount) | 列：Q10<br>过滤：Q10<br>聚合：Q10 |
| Q10 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT * FROM sheet1 LIMIT 20
```

### Q2（成功）

```sql
SELECT COUNT(*) AS row_count, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Sales Month") AS n_months, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month FROM sheet1
```

### Q3（成功）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales
FROM sheet1
GROUP BY "Sales Month", "Product Code"
ORDER BY "Sales Month", total_sales DESC
```

### Q4（成功）

```sql
SELECT * FROM (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month" ORDER BY SUM("Sales Amount") DESC) AS rnk
  FROM sheet1
  GROUP BY "Sales Month", "Product Code"
) WHERE rnk = 1
ORDER BY "Sales Month"
```

### Q5（成功）

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions, COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"
```

### Q6（成功）

```sql
SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit"
```

### Q7（成功）

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

### Q8（成功）

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

### Q9（成功）

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

### Q10（成功）

```sql
SELECT "Product Code", SUM("Sales Amount") AS total_sales,
       COUNT(DISTINCT "Customer ID") AS total_customers,
       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```
