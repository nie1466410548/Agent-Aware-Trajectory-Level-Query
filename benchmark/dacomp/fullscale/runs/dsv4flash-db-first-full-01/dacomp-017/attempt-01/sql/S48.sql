
SELECT "Customer ID", substr("Order Date",1,4) AS yr, 
       "Order ID", "Quantity", "Product", Sales, profit,
       profit * 1.0 / Sales AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
  AND "Quantity" != 'abc'
  AND "Quantity" IS NOT NULL
