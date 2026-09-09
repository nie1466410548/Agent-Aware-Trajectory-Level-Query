SELECT c.gender, COUNT(o."Order ID") AS orders, COUNT(DISTINCT o."Customer ID") AS customers, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit, SUM(o.profit)/COUNT(DISTINCT o."Customer ID") AS profit_per_customer
FROM order_information o JOIN customer_information c ON o."Customer ID" = c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender ORDER BY profit DESC