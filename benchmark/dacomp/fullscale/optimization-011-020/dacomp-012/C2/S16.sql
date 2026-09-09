WITH b AS (
  SELECT
    *
  FROM temp."reuse_012_c2"
)
SELECT
  interval AS "interval",
  cut AS "cut",
  COUNT(*) AS "n",
  ROUND(AVG(price / carat), 2) AS "avg_ppc"
FROM b
GROUP BY
  interval,
  cut
ORDER BY
  interval,
  avg_ppc DESC;
