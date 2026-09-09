SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Order ID" AS "Order ID",
  "Quantity" AS "Quantity",
  "Product" AS "Product",
  Sales AS "Sales",
  profit AS "profit",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;
