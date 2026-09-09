SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  COUNT(*) AS "n",
  ROUND(SUM(Sales), 0) AS "total_sales",
  ROUND(SUM(profit), 1) AS "total_profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  "Product",
  yr;
