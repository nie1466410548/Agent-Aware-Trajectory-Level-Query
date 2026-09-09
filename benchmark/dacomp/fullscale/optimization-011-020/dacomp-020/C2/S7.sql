SELECT
  __g0 AS "mh",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 3) AS "avg_exam",
  ROUND(
    (
      1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
    ) - (
      1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
    ) * (
      1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
    ),
    3
  ) AS "var_exam"
FROM temp."reuse_020_c2"
GROUP BY
  __g0
ORDER BY
  mh;
