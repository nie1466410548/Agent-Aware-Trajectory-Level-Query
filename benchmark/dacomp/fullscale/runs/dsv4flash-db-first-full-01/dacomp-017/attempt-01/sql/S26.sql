SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales,
       SUM(Sales)*1.0 / SUM(SUM(Sales)) OVER (PARTITION BY substr("Order Date",1,4)) AS sales_share
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales_share DESC