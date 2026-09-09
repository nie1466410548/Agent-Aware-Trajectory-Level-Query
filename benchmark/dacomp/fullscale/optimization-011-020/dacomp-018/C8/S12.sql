SELECT
  COUNT(*) AS "total_fashion_customers",
  COUNT(DISTINCT "Customer ID") AS "distinct_fashion_customers"
FROM temp."reuse_018_c8" AS order_information
WHERE
  "Product Category" = 'Fashion';
