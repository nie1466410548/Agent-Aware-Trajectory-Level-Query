
SELECT "Product Category", "Product", Sales, profit, "Quantity"
FROM order_information
WHERE "Quantity" != 'abc' AND "Quantity" IS NOT NULL
