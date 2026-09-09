-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_012_c1" AS
SELECT "Price (USD)" AS price, "Carat (diamond weight)" AS carat, CASE WHEN "Carat (diamond weight)" <= 0.5 THEN 'A: <=0.5 ct' WHEN "Carat (diamond weight)" <= 1.0 THEN 'B: 0.51-1.0 ct' WHEN "Carat (diamond weight)" <= 1.5 THEN 'C: 1.01-1.5 ct' ELSE 'D: >1.5 ct' END AS interval FROM sheet1;

-- S9
WITH buckets AS (
  SELECT
    *
  FROM temp."reuse_012_c1"
)
SELECT
  interval AS "interval",
  carat AS "q",
  price_per_carat AS "price_per_carat"
FROM (
  SELECT
    interval,
    carat,
    price / carat AS price_per_carat,
    ROW_NUMBER() OVER (PARTITION BY interval ORDER BY price / carat) AS rn,
    COUNT(*) OVER (PARTITION BY interval) AS cnt
  FROM buckets
)
WHERE
  rn IN ((
      cnt + 1
    ) / 2, (
      cnt + 2
  ) / 2)
ORDER BY
  interval,
  q;

-- S10
WITH buckets AS (
  SELECT
    *
  FROM temp."reuse_012_c1"
)
SELECT
  interval AS "interval",
  COUNT(*) AS "n",
  ROUND(AVG(carat), 3) AS "avg_carat",
  ROUND(AVG(price), 2) AS "avg_price",
  ROUND(AVG(price / carat), 2) AS "avg_ppc",
  ROUND(MIN(price / carat), 2) AS "min_ppc",
  ROUND(MAX(price / carat), 2) AS "max_ppc",
  ROUND(
    SQRT(
      AVG((
        price / carat
      ) * (
        price / carat
      )) - AVG(price / carat) * AVG(price / carat)
    ),
    2
  ) AS "sd_ppc",
  ROUND(
    AVG(price / carat) / SQRT(
      AVG((
        price / carat
      ) * (
        price / carat
      )) - AVG(price / carat) * AVG(price / carat)
    ),
    2
  ) AS "cv"
FROM buckets
GROUP BY
  interval
ORDER BY
  interval;

DROP TABLE temp."reuse_012_c1";
