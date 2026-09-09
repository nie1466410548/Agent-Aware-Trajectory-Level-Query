-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c14" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Discount" <> 'xxx' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL;

-- S65
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  AVG(CAST("Discount" AS REAL)) AS "avg_discount",
  AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS "avg_qty_discount"
FROM temp."reuse_017_c14" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Discount" <> 'xxx'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
GROUP BY
  yr
ORDER BY
  yr;

-- S66
SELECT
  "Product" AS "Product",
  AVG(CAST("Discount" AS REAL)) AS "avg_discount",
  AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS "avg_qty_discount"
FROM temp."reuse_017_c14" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Discount" <> 'xxx'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
GROUP BY
  "Product"
ORDER BY
  avg_qty_discount DESC;

DROP TABLE temp."reuse_017_c14";
