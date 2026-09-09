-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- BUILD C3 before S3
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

-- S9
WITH buckets AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN 'A: <=0.5 ct'
      WHEN "Carat (diamond weight)" <= 1.0 THEN 'B: 0.51-1.0 ct'
      WHEN "Carat (diamond weight)" <= 1.5 THEN 'C: 1.01-1.5 ct'
      ELSE 'D: >1.5 ct'
    END AS interval
  FROM sheet1
)
SELECT interval, carat AS q, price_per_carat
FROM (
  SELECT interval, carat, price/carat AS price_per_carat,
    ROW_NUMBER() OVER (PARTITION BY interval ORDER BY price/carat) AS rn,
    COUNT(*) OVER (PARTITION BY interval) AS cnt
  FROM buckets
)
WHERE rn IN ((cnt+1)/2, (cnt+2)/2)
ORDER BY interval, q;

-- S10
WITH buckets AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN 'A: <=0.5 ct'
      WHEN "Carat (diamond weight)" <= 1.0 THEN 'B: 0.51-1.0 ct'
      WHEN "Carat (diamond weight)" <= 1.5 THEN 'C: 1.01-1.5 ct'
      ELSE 'D: >1.5 ct'
    END AS interval
  FROM sheet1
)
SELECT 
  interval,
  COUNT(*) AS n,
  ROUND(AVG(carat),3) AS avg_carat,
  ROUND(AVG(price),2) AS avg_price,
  ROUND(AVG(price/carat),2) AS avg_ppc,
  ROUND(MIN(price/carat),2) AS min_ppc,
  ROUND(MAX(price/carat),2) AS max_ppc,
  ROUND(sqrt(AVG((price/carat)*(price/carat)) - AVG(price/carat)*AVG(price/carat)),2) AS sd_ppc,
  ROUND(AVG(price/carat)/sqrt(AVG((price/carat)*(price/carat)) - AVG(price/carat)*AVG(price/carat)),2) AS cv
FROM buckets
GROUP BY interval
ORDER BY interval;

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

-- S16
WITH b AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    "Cut (quality)" AS cut,
    "Color" AS color,
    "Clarity" AS clarity,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN '<=0.5'
      WHEN "Carat (diamond weight)" <= 1.0 THEN '0.51-1.0'
      WHEN "Carat (diamond weight)" <= 1.5 THEN '1.01-1.5'
      ELSE '>1.5'
    END AS interval
  FROM sheet1
)
SELECT interval, cut, COUNT(*) AS n, ROUND(AVG(price/carat),2) AS avg_ppc
FROM b
GROUP BY interval, cut
ORDER BY interval, avg_ppc DESC;

-- S17
WITH b AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    "Cut (quality)" AS cut,
    "Color" AS color,
    "Clarity" AS clarity,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN '<=0.5'
      WHEN "Carat (diamond weight)" <= 1.0 THEN '0.51-1.0'
      WHEN "Carat (diamond weight)" <= 1.5 THEN '1.01-1.5'
      ELSE '>1.5'
    END AS interval
  FROM sheet1
)
SELECT interval, color, COUNT(*) AS n, ROUND(AVG(price/carat),2) AS avg_ppc
FROM b
GROUP BY interval, color
ORDER BY interval, color;

-- S18
WITH b AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    "Cut (quality)" AS cut,
    "Color" AS color,
    "Clarity" AS clarity,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN '<=0.5'
      WHEN "Carat (diamond weight)" <= 1.0 THEN '0.51-1.0'
      WHEN "Carat (diamond weight)" <= 1.5 THEN '1.01-1.5'
      ELSE '>1.5'
    END AS interval
  FROM sheet1
)
SELECT interval, clarity, COUNT(*) AS n, ROUND(AVG(price/carat),2) AS avg_ppc
FROM b
GROUP BY interval, clarity
ORDER BY interval, clarity;

-- S19
SELECT * FROM sheet1 LIMIT 5;

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

-- S21
WITH s AS (
  SELECT "Price (USD)" AS price, "Carat (diamond weight)" AS carat, "Depth percentage" AS depth,
         "Table percentage" AS tbl, "X-axis length (mm)" AS x, "Y-axis width (mm)" AS y, "Z-axis depth (mm)" AS z
  FROM sheet1
)
SELECT 'carat' AS var, ROUND((AVG(carat*price) - AVG(carat)*AVG(price)) / 
    (sqrt(AVG(carat*carat) - AVG(carat)*AVG(carat)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) AS corr_with_price
FROM s
UNION ALL
SELECT 'depth', ROUND((AVG(depth*price) - AVG(depth)*AVG(price)) / 
    (sqrt(AVG(depth*depth) - AVG(depth)*AVG(depth)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'table', ROUND((AVG(tbl*price) - AVG(tbl)*AVG(price)) / 
    (sqrt(AVG(tbl*tbl) - AVG(tbl)*AVG(tbl)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'x', ROUND((AVG(x*price) - AVG(x)*AVG(price)) / 
    (sqrt(AVG(x*x) - AVG(x)*AVG(x)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'y', ROUND((AVG(y*price) - AVG(y)*AVG(price)) / 
    (sqrt(AVG(y*y) - AVG(y)*AVG(y)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'z', ROUND((AVG(z*price) - AVG(z)*AVG(price)) / 
    (sqrt(AVG(z*z) - AVG(z)*AVG(z)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'log(price) vs log(carat)', ROUND((AVG(ln(carat)*ln(price)) - AVG(ln(carat))*AVG(ln(price))) / 
    (sqrt(AVG(ln(carat)*ln(carat)) - AVG(ln(carat))*AVG(ln(carat))) * sqrt(AVG(ln(price)*ln(price)) - AVG(ln(price))*AVG(ln(price)))), 4) FROM s;

-- S22
SELECT "Carat (diamond weight)" AS carat, "Cut (quality)" AS cut, "Color" AS color,
         "Clarity" AS clarity, "Depth percentage" AS depth, "Table percentage" AS tbl,
         "Price (USD)" AS price
  FROM sheet1;

DROP TABLE temp."reuse_012_c3";
COMMIT;
