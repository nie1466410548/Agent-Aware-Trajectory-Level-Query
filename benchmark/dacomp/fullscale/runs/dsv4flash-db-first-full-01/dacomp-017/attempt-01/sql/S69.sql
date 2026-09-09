
SELECT "Customer ID", SUM(profit) AS profit, SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Customer ID"
