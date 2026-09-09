SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";
