-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c3" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product Category" AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2, SUM(CASE WHEN "Discount" = 'xxx' OR "Quantity" = 'abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) AS __a5, MAX("Order Date") AS __a6, MIN("Order Date") AS __a7 FROM "order_information"  GROUP BY SUBSTRING("Order Date", 1, 4), "Product Category";

-- S5
SELECT
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3";

-- S8
SELECT
  __g0 AS "yr",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3"
GROUP BY
  __g0;

-- S9
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a1) AS "total_profit",
  SUM(__a2) AS "total_sales",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "profit_margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S10
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 6) AS "pm"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S13
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a3) AS "bad_rows",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S14
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a4) AS "neg_rows",
  SUM(__a0) AS "n",
  SUM(__a5) AS "neg_profit"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S42
SELECT
  MAX(__a6) AS "max_date",
  MIN(__a7) AS "min_date"
FROM temp."reuse_017_c3";

-- S57
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a1) * 1.0 / SUM(__a2) AS "margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S68
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

DROP TABLE temp."reuse_017_c3";
