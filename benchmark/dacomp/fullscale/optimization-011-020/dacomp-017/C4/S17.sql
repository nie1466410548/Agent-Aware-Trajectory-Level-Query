SELECT
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  ROUND(AVG(profit * 1.0 / Sales), 4) AS "avg_margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Discount"
ORDER BY
  "Discount";
