-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_015_c4" AS
SELECT "Floor Plan" AS __g0, floor AS __g1, decoration AS __g2, orientation AS __g3, "Watch Count" AS __g4, featured AS __g5, "Date Published" AS __g6, COUNT(*) AS __a0, SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) AS __a6, SUM("Watch Count") AS __a7_sum, COUNT("Watch Count") AS __a7_n, SUM(showings) AS __a8_sum, COUNT(showings) AS __a8_n, MAX("Watch Count") AS __a9, MAX(showings) AS __a10, MIN("Watch Count") AS __a11, MIN(showings) AS __a12 FROM "data"  GROUP BY "Floor Plan", floor, decoration, orientation, "Watch Count", featured, "Date Published";

-- S4
SELECT
  SUM(__a0) AS "COUNT(*)"
FROM temp."reuse_015_c4";

-- S9
SELECT
  __g0 AS "Floor Plan",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g0
ORDER BY
  cnt DESC;

-- S10
SELECT
  __g1 AS "Floor",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g1
ORDER BY
  cnt DESC;

-- S11
SELECT
  __g2 AS "Decoration",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g2
ORDER BY
  cnt DESC;

-- S12
SELECT
  __g3 AS "Orientation",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g3
ORDER BY
  cnt DESC;

-- S13
SELECT
  __g1 AS "Floor",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g1
ORDER BY
  __g1;

-- S15
SELECT
  __g1 AS "Floor",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g1
ORDER BY
  __g1;

-- S17
SELECT
  __g0 AS "Floor Plan",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g0
ORDER BY
  cnt DESC;

-- S18
SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "watch_gt0",
  SUM(__a2) AS "watch_eq0",
  SUM(__a3) AS "watch_gt50",
  SUM(__a4) AS "show_gt0",
  SUM(__a5) AS "show_eq0",
  SUM(__a6) AS "show_gt10",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_watch",
  (
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ) AS "avg_show",
  MAX(__a9) AS "max_watch",
  MAX(__a10) AS "max_show",
  MIN(__a11) AS "min_watch",
  MIN(__a12) AS "min_show"
FROM temp."reuse_015_c4";

-- S19
SELECT
  __g4 AS "Watch Count",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g4
ORDER BY
  __g4 DESC
LIMIT 20;

-- S28
SELECT
  __g5 AS "Featured",
  SUM(__a0) AS "cnt",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_watch",
  (
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ) AS "avg_show"
FROM temp."reuse_015_c4"
GROUP BY
  __g5;

-- S29
SELECT
  __g6 AS "Date Published",
  SUM(__a0) AS "cnt",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_watch",
  (
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ) AS "avg_show"
FROM temp."reuse_015_c4"
GROUP BY
  __g6
ORDER BY
  cnt DESC;

DROP TABLE temp."reuse_015_c4";
