
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales DESC
