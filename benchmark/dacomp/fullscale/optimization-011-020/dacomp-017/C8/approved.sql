-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c8" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';

-- S36
SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';

-- S37
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

-- S39
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

DROP TABLE temp."reuse_017_c8";
