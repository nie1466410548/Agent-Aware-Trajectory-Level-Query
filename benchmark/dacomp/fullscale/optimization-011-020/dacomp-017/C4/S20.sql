SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  ROUND(SUM(profit), 1) AS "total_profit",
  ROUND(SUM(Sales), 1) AS "total_sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 6) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Discount"
ORDER BY
  yr,
  "Discount";
