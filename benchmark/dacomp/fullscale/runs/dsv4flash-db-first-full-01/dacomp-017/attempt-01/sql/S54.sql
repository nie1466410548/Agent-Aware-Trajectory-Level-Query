SELECT "Product", "Quantity", Sales, profit, profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Towels'
ORDER BY "Quantity", Sales
LIMIT 30