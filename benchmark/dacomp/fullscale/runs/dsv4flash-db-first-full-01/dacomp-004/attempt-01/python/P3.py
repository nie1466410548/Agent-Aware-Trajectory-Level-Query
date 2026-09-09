import os
for f in ['top_products_monthly.png', 'repurchase_vs_sales_scatter.png', 'top_products_repurchase_vs_sales.png']:
    p = f'/work/{f}'
    print(p, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else '')

# Summary stats on repurchase rate distribution
res = db.query("""
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
""")
df = db.frame(res)
print("\nRepurchase rate distribution (products with >=5 customers):")
print(df['repurchase_rate'].describe())
print("\nQuantiles of repurchase rate:")
print(df['repurchase_rate'].quantile([0.25, 0.5, 0.75, 0.9, 0.95]))

# Top-10 products by total sales with their repurchase rates
res2 = db.query("""
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
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code" AS product, ROUND(s.total_sales,2) AS total_sales,
       s.n_transactions, ps.n_customers,
       ROUND(1.0 * ps.repeat_customers / NULLIF(ps.n_customers,0), 4) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
ORDER BY s.total_sales DESC
LIMIT 10
""")
print("\nTop 10 products by total sales (>=5 customers):")
print(db.frame(res2).to_string(index=False))