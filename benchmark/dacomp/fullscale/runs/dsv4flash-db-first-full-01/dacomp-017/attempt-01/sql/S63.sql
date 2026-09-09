
SELECT "Customer ID", substr("Order Date",1,4) AS yr, profit, Sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
