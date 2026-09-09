WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, CAST(o.Discount AS REAL) AS discount, COUNT(*) AS orders, SUM(o.profit) AS profit,
  AVG(o.profit) AS avg_profit, SUM(o.Sales) AS sales
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, discount ORDER BY c.gender, discount