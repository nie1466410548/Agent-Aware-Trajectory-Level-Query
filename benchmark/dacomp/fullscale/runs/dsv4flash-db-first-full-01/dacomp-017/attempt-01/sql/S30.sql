SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"