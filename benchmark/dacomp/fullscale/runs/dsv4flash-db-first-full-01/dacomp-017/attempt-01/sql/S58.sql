
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY "Product", yr
