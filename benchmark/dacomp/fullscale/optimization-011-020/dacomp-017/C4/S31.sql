SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Order Priority" AS "Order Priority",
  COUNT(*) AS "n"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Order Priority"
ORDER BY
  yr,
  "Order Priority";
