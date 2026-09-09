-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_012_c3" AS
SELECT "Cut (quality)" AS __g0, color AS __g1, clarity AS __g2, COUNT(*) AS __a0, SUM(CASE WHEN "Carat (diamond weight)" IS NULL THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Cut (quality)" IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Color" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Clarity" IS NULL THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN "Depth percentage" IS NULL THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN "Table percentage" IS NULL THEN 1 ELSE 0 END) AS __a6, SUM(CASE WHEN "X-axis length (mm)" IS NULL THEN 1 ELSE 0 END) AS __a7, SUM(CASE WHEN "Y-axis width (mm)" IS NULL THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Z-axis depth (mm)" IS NULL THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN "Price (USD)" IS NULL THEN 1 ELSE 0 END) AS __a10, MIN("Price (USD)") AS __a11, MAX("Price (USD)") AS __a12, SUM("Price (USD)") AS __a13_sum, COUNT("Price (USD)") AS __a13_n, MIN("Carat (diamond weight)") AS __a14, MAX("Carat (diamond weight)") AS __a15, SUM("Carat (diamond weight)") AS __a16_sum, COUNT("Carat (diamond weight)") AS __a16_n, SUM("Price (USD)" / "Carat (diamond weight)") AS __a17_sum, COUNT("Price (USD)" / "Carat (diamond weight)") AS __a17_n, SUM("Depth percentage") AS __a18_sum, COUNT("Depth percentage") AS __a18_n, SUM("Table percentage") AS __a19_sum, COUNT("Table percentage") AS __a19_n, SUM("Carat (diamond weight)" * "Price (USD)") AS __a20_sum, COUNT("Carat (diamond weight)" * "Price (USD)") AS __a20_n, SUM("Carat (diamond weight)" * "Carat (diamond weight)") AS __a21_sum, COUNT("Carat (diamond weight)" * "Carat (diamond weight)") AS __a21_n, SUM("Price (USD)" * "Price (USD)") AS __a22_sum, COUNT("Price (USD)" * "Price (USD)") AS __a22_n FROM "sheet1"  GROUP BY "Cut (quality)", color, clarity;

-- S3
SELECT
  SUM(__a0) AS "total_rows"
FROM temp."reuse_012_c3";

-- S4
SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "null_carat",
  SUM(__a2) AS "null_cut",
  SUM(__a3) AS "null_color",
  SUM(__a4) AS "null_clarity",
  SUM(__a5) AS "null_depth",
  SUM(__a6) AS "null_table",
  SUM(__a7) AS "null_x",
  SUM(__a8) AS "null_y",
  SUM(__a9) AS "null_z",
  SUM(__a10) AS "null_price"
FROM temp."reuse_012_c3";

-- S5
SELECT
  __g0 AS "cut",
  SUM(__a0) AS "n",
  MIN(__a11) AS "min_price",
  MAX(__a12) AS "max_price",
  (
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ) AS "avg_price"
FROM temp."reuse_012_c3"
GROUP BY
  __g0
ORDER BY
  n DESC;

-- S6
SELECT
  __g1 AS "Color",
  SUM(__a0) AS "n"
FROM temp."reuse_012_c3"
GROUP BY
  __g1
ORDER BY
  __g1;

-- S7
SELECT
  __g2 AS "Clarity",
  SUM(__a0) AS "n"
FROM temp."reuse_012_c3"
GROUP BY
  __g2
ORDER BY
  __g2;

-- S11
SELECT
  MIN(__a14) AS "min_carat",
  MAX(__a15) AS "max_carat",
  MIN(__a11) AS "min_price",
  MAX(__a12) AS "max_price",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 2) AS "avg_price",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a18_sum) / NULLIF(SUM(__a18_n), 0)
  ), 2) AS "avg_depth",
  ROUND((
    1.0 * SUM(__a19_sum) / NULLIF(SUM(__a19_n), 0)
  ), 2) AS "avg_table"
FROM temp."reuse_012_c3";

-- S13
SELECT
  __g0 AS "cut",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat"
FROM temp."reuse_012_c3"
GROUP BY
  __g0
ORDER BY
  avg_ppc DESC;

-- S14
SELECT
  __g1 AS "Color",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat"
FROM temp."reuse_012_c3"
GROUP BY
  __g1
ORDER BY
  __g1;

-- S15
SELECT
  __g2 AS "Clarity",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat"
FROM temp."reuse_012_c3"
GROUP BY
  __g2
ORDER BY
  __g2;

-- S20
SELECT
  ROUND(
    (
      1.0 * SUM(__a20_sum) / NULLIF(SUM(__a20_n), 0)
    ) - (
      1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
    ) * (
      1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
    ),
    4
  ) AS "carat_price_cov",
  ROUND(
    (
      (
        1.0 * SUM(__a20_sum) / NULLIF(SUM(__a20_n), 0)
      ) - (
        1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
      ) * (
        1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
      )
    ) / (
      SQRT(
        (
          1.0 * SUM(__a21_sum) / NULLIF(SUM(__a21_n), 0)
        ) - (
          1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
        ) * (
          1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
        )
      ) * SQRT(
        (
          1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
        ) - (
          1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
        ) * (
          1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
        )
      )
    ),
    4
  ) AS "corr_carat_price"
FROM temp."reuse_012_c3";

DROP TABLE temp."reuse_012_c3";
