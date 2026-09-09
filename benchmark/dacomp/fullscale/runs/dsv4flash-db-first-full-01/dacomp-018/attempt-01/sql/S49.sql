
WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT c.gender, strftime('%Y-%m', o."Order Date") AS ym, SUM(o.profit) AS profit, COUNT(*) AS orders
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, ym
