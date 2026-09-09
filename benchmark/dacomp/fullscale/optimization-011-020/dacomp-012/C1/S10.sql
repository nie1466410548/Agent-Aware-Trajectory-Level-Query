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
