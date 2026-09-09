-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c9" AS
SELECT "Quantity" AS __g0, SUBSTRING("Order Date", 1, 4) AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2 FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas' GROUP BY "Quantity", SUBSTRING("Order Date", 1, 4);

-- S37
SELECT
  __g0 AS "Quantity",
  SUM(__a0) AS "n",
  SUM(__a1) AS "profit",
  SUM(__a2) AS "sales",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "margin"
FROM temp."reuse_017_c9"
GROUP BY
  __g0
ORDER BY
  __g0;

-- S39
SELECT
  __g1 AS "yr",
  __g0 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c9"
GROUP BY
  __g1,
  __g0
ORDER BY
  yr,
  __g0;

DROP TABLE temp."reuse_017_c9";
