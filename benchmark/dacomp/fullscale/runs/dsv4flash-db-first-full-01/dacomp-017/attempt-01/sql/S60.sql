
SELECT profit, Sales, "Quantity", "Discount"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
LIMIT 5000
