WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
ranked AS (
  SELECT profit, NTILE(5) OVER (ORDER BY profit DESC) AS quintile
  FROM cust_orders
)
SELECT quintile, COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)*100.0/(SELECT SUM(profit) FROM cust_orders) AS pct_of_profit
FROM ranked GROUP BY quintile ORDER BY quintile