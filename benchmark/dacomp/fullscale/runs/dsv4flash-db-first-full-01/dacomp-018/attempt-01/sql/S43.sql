WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, strftime('%Y', o."Order Date") AS year, strftime('%m', o."Order Date") AS month,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, year, month ORDER BY year, month, c.gender