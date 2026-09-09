WITH cust AS (
  SELECT "Customer ID", gender
  FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, EXTRACT(YEAR FROM o."Order Date") AS year, EXTRACT(MONTH FROM o."Order Date") AS month,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, year, month ORDER BY year, month, c.gender