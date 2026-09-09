SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  "Discount" AS "Discount",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx';
