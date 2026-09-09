-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c11" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL;

-- S48
SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Order ID" AS "Order ID",
  "Quantity" AS "Quantity",
  "Product" AS "Product",
  Sales AS "Sales",
  profit AS "profit",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

-- S50
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

-- S51
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

-- S52
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

-- S59
SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

-- S62
SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity"
FROM temp."reuse_017_c11" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL;

DROP TABLE temp."reuse_017_c11";
