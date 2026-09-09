SELECT
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';
