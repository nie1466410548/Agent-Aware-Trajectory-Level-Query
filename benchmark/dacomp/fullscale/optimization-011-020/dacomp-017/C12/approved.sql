-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c12" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers';

-- S53
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c12" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers'
ORDER BY
  "Quantity",
  Sales
LIMIT 30;

-- S55
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c12" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers'
ORDER BY
  "Quantity",
  "Discount";

DROP TABLE temp."reuse_017_c12";
