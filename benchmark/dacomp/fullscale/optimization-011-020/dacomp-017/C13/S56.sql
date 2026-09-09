SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  "Shipping Cost" AS "Shipping Cost"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx';
