
SELECT COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit
FROM order_information WHERE "Product Category" = 'Home & Furniture'
