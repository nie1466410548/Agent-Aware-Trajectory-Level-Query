WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT COUNT(*) AS top10_customers, SUM(profit) AS top10_profit, SUM(profit) * 100.0 / (SELECT SUM(profit) FROM cust_orders) AS pct_of_total_profit
FROM (SELECT "Customer ID", profit FROM cust_orders ORDER BY profit DESC LIMIT 80)