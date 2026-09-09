SELECT
  "Product" AS "Product",
  COUNT(*) AS "orders",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  AVG(profit) AS "avg_profit_per_order"
FROM temp."reuse_018_c8" AS order_information
WHERE
  "Product Category" = 'Fashion'
GROUP BY
  "Product"
ORDER BY
  profit DESC;
