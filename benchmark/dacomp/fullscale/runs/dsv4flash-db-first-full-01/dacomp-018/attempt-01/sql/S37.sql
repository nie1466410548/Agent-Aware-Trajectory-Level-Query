WITH cust AS (
  SELECT "Customer ID", gender, "Customer Segment"
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, COUNT(*) AS customers, COUNT(*)*100.0/795 AS pct_of_customers,
  SUM(co.profit) AS profit, SUM(co.profit)*100.0/(SELECT SUM(profit) FROM cust_orders) AS pct_of_profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
GROUP BY c.gender