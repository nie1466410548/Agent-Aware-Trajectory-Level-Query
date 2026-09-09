SELECT substr("Order Date",1,4) AS yr, "Discount", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Discount"
ORDER BY yr, "Discount"