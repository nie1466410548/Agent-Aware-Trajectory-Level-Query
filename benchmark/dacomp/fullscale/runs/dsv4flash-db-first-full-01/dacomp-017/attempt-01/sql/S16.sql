SELECT "Order ID", "Product Category", "Product", Sales, "Discount", profit, profit*1.0/Sales AS order_margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Discount" = 'xxx'
LIMIT 20