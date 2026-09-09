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
