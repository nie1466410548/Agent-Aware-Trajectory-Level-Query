WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, o."Shipping Method", COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Shipping Method" ORDER BY c.gender, orders DESC