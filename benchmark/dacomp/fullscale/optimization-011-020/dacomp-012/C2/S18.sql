WITH b AS (
  SELECT
    *
  FROM temp."reuse_012_c2"
)
SELECT
  interval AS "interval",
  clarity AS "clarity",
  COUNT(*) AS "n",
  ROUND(AVG(price / carat), 2) AS "avg_ppc"
FROM b
GROUP BY
  interval,
  clarity
ORDER BY
  interval,
  clarity;
