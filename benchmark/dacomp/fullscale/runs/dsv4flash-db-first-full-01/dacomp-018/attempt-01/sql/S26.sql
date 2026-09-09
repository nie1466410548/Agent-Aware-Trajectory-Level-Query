SELECT "Product", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit, AVG(profit) AS avg_profit_per_order
FROM order_information WHERE "Product Category" = 'Fashion'
GROUP BY "Product" ORDER BY profit DESC