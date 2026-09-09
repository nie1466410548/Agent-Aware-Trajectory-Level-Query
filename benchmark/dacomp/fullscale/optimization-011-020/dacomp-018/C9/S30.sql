SELECT
  COUNT(*) AS "rows_cnt",
  COUNT(DISTINCT "Customer ID") AS "customers"
FROM temp."reuse_018_c9" AS product_browsing
WHERE
  "Product Category" = 'Fashion';
