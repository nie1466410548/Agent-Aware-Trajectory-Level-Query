
SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
