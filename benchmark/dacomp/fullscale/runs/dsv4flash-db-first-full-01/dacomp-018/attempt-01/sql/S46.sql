WITH cust AS (
  SELECT "Customer ID", gender, "Customer Segment", age, "Education Level", "Marital Status", Region
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment", c.Region,
  COUNT(*) AS customers, SUM(co.profit) AS profit, SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
GROUP BY c.gender, c."Customer Segment", c.Region
ORDER BY profit_per_customer DESC LIMIT 20