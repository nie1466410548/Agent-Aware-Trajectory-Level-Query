SELECT
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(profit) AS "profit",
  SUM(Sales) AS "sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY
  "Quantity"
ORDER BY
  "Quantity";
