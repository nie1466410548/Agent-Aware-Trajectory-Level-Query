SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Discount" AS "Discount",
  COUNT(*) AS "n"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Discount"
ORDER BY
  yr,
  "Discount";
