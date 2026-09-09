
SELECT "Product", "Quantity", "Discount", Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' 
  AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
