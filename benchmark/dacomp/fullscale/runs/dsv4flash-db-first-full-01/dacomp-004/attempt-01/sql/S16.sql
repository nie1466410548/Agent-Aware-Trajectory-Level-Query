
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
  SELECT "Product Code", SUM("Sales Amount") AS total_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s.total_sales, 1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
