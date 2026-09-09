SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  SUM(Sales) AS "sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  yr,
  sales DESC;
