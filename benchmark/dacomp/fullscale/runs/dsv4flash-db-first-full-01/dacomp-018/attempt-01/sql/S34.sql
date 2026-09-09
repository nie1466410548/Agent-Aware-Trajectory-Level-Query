WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
ranked AS (
  SELECT c.*, co.profit, co.orders, co.sales, NTILE(10) OVER (ORDER BY co.profit DESC) AS decile
  FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
)
SELECT gender, "Customer Segment", COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)/COUNT(*) AS avg_profit
FROM ranked WHERE decile = 1
GROUP BY gender, "Customer Segment" ORDER BY avg_profit DESC