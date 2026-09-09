SELECT
  "Shipping Method" AS "Shipping Method",
  COUNT(*) AS "n",
  SUM(profit) AS "total_profit",
  SUM(Sales) AS "total_sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Shipping Method"
ORDER BY
  "Shipping Method";
