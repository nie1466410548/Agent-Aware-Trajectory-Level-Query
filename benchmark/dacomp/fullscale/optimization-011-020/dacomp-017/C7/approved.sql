-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c7" AS
SELECT "Quantity" AS __g0, "Discount" AS __g1, SUBSTRING("Order Date", 1, 4) AS __g2, COUNT(*) AS __a0, SUM(sales) AS __a1, SUM(profit) AS __a2 FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds' GROUP BY "Quantity", "Discount", SUBSTRING("Order Date", 1, 4);

-- S32
SELECT
  __g0 AS "Quantity",
  __g1 AS "Discount",
  SUM(__a0) AS "n",
  SUM(__a1) AS "sales",
  SUM(__a2) AS "profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a1), 4) AS "margin"
FROM temp."reuse_017_c7"
GROUP BY
  __g0,
  __g1
ORDER BY
  __g0,
  __g1;

-- S34
SELECT
  __g0 AS "Quantity",
  SUM(__a0) AS "n",
  SUM(__a1) AS "sales",
  SUM(__a2) AS "profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a1), 4) AS "margin"
FROM temp."reuse_017_c7"
GROUP BY
  __g0
ORDER BY
  __g0;

-- S35
SELECT
  __g2 AS "yr",
  __g0 AS "Quantity",
  SUM(__a0) AS "n",
  SUM(__a1) AS "sales",
  SUM(__a2) AS "profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a1), 4) AS "margin"
FROM temp."reuse_017_c7"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;

-- S38
SELECT
  __g2 AS "yr",
  __g0 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c7"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;

DROP TABLE temp."reuse_017_c7";
