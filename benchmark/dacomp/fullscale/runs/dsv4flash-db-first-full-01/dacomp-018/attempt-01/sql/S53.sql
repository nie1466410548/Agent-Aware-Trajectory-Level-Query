WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, strftime('%m', o."Order Date") AS month_num, o."Month" AS month_name,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, month_num, month_name ORDER BY month_num, c.gender