SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;
