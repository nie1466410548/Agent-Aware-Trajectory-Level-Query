SELECT
  "Discount" AS "Discount",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  COUNT(*) AS "n",
  AVG(profit * 1.0 / Sales) AS "avg_margin",
  AVG(profit) AS "avg_profit",
  AVG(Sales) AS "avg_sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Discount",
  yr
ORDER BY
  "Discount",
  yr;
