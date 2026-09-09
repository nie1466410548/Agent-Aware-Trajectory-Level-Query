SELECT
  COUNT(DISTINCT "Customer ID") AS "n_customers"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';
