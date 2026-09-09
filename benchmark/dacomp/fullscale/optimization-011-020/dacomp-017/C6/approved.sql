-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c6" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';

-- S27
SELECT * FROM temp."reuse_017_c6" AS order_information WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds' LIMIT 10;

-- S32
SELECT
  "Quantity" AS "Quantity",
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  "Quantity",
  "Discount"
ORDER BY
  "Quantity",
  "Discount";

-- S33
SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';

-- S34
SELECT
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  "Quantity"
ORDER BY
  "Quantity";

-- S35
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

-- S38
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

DROP TABLE temp."reuse_017_c6";
