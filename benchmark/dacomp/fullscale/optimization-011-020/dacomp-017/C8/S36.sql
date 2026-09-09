SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';
