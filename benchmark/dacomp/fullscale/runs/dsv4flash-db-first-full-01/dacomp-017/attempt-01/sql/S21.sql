SELECT "Product", COUNT(*) AS n, SUM(Sales) AS total_sales, SUM(profit) AS total_profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),6) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product"
ORDER BY margin