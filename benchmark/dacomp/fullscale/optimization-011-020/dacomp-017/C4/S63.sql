SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  profit AS "profit",
  Sales AS "Sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';
