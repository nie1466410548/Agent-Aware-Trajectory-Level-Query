
SELECT COUNT(DISTINCT "Order ID") AS distinct_orders, COUNT(*) AS rows_count
FROM order_information WHERE "Product Category" = 'Home & Furniture'
