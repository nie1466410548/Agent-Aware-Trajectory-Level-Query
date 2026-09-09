SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";
