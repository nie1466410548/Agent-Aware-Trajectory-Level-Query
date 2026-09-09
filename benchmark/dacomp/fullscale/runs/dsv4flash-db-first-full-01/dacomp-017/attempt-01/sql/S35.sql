SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"