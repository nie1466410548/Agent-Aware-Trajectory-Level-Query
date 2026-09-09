-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_018_c8" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Fashion';

-- S8
SELECT * FROM temp."reuse_018_c8" AS order_information WHERE "Product Category" = 'Fashion' LIMIT 5;

-- S12
SELECT
  COUNT(*) AS "total_fashion_customers",
  COUNT(DISTINCT "Customer ID") AS "distinct_fashion_customers"
FROM temp."reuse_018_c8" AS order_information
WHERE
  "Product Category" = 'Fashion';

-- S26
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

-- S44
SELECT DISTINCT
  STRFTIME('%Y-%m', "Order Date") AS "ym"
FROM temp."reuse_018_c8" AS order_information
WHERE
  "Product Category" = 'Fashion'
ORDER BY
  ym;

DROP TABLE temp."reuse_018_c8";
