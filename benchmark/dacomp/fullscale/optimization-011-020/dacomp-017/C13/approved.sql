-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c13" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL AND "Discount" <> 'xxx';

-- S56
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  "Shipping Cost" AS "Shipping Cost"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx';

-- S60
SELECT
  profit AS "profit",
  Sales AS "Sales",
  "Quantity" AS "Quantity",
  "Discount" AS "Discount"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx'
LIMIT 5000;

-- S67
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  "Discount" AS "Discount",
  Sales AS "Sales",
  profit AS "profit"
FROM temp."reuse_017_c13" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
  AND "Discount" <> 'xxx';

DROP TABLE temp."reuse_017_c13";
