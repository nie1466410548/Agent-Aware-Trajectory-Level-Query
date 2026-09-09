WITH cust AS (
  SELECT "Customer ID", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.Country, COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.Country ORDER BY profit DESC