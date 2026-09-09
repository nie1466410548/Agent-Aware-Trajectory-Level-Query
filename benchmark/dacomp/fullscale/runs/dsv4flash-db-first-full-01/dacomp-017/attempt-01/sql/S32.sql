SELECT "Quantity", "Discount", COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY "Quantity", "Discount"
ORDER BY "Quantity", "Discount"