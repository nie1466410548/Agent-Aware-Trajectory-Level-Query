WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions, COUNT(DISTINCT "Customer ID") AS n_cust_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code",
       ROUND(s.total_sales, 2) AS total_sales,
       s.n_transactions,
       ps.n_customers,
       ps.repeat_customers,
       ROUND(1.0 * ps.repeat_customers / ps.n_customers, 4) AS repurchase_rate
FROM sales s
JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
ORDER BY s.total_sales DESC
LIMIT 30