SELECT
  profit AS "profit",
  Sales AS "Sales",
  "Quantity" AS "Quantity",
  "Discount" AS "Discount"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx'
LIMIT 5000;
