WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, o."Order Priority", COUNT(*) AS orders, SUM(o.profit) AS profit, SUM(o.profit)/COUNT(*) AS avg_profit_per_order
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Order Priority" ORDER BY c.gender, orders DESC