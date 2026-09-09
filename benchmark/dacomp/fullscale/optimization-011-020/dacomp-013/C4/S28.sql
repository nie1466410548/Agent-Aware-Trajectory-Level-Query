SELECT
  __g0 AS "Task Status",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 1) AS "avg_planned"
FROM temp."reuse_013_c4"
GROUP BY
  __g0
ORDER BY
  __g0;
