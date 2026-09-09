SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';
