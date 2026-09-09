SELECT substr("Order Date",1,4) AS yr, "Order Priority", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Order Priority"
ORDER BY yr, "Order Priority"