
SELECT "Product Category", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
