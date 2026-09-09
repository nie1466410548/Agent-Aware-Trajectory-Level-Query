-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c15" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product" AS __g1, SUM(CAST("Discount" AS REAL)) AS __a0_sum, COUNT(CAST("Discount" AS REAL)) AS __a0_n, SUM(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_sum, COUNT(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_n FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Discount" <> 'xxx' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL GROUP BY SUBSTRING("Order Date", 1, 4), "Product";

-- S65
SELECT
  __g0 AS "yr",
  (
    1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)
  ) AS "avg_discount",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_qty_discount"
FROM temp."reuse_017_c15"
GROUP BY
  __g0
ORDER BY
  yr;

-- S66
SELECT
  __g1 AS "Product",
  (
    1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)
  ) AS "avg_discount",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_qty_discount"
FROM temp."reuse_017_c15"
GROUP BY
  __g1
ORDER BY
  avg_qty_discount DESC;

DROP TABLE temp."reuse_017_c15";
