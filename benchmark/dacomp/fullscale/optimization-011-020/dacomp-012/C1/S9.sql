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
