SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  SUM(profit) * 1.0 / SUM(Sales) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  "Product",
  yr;
