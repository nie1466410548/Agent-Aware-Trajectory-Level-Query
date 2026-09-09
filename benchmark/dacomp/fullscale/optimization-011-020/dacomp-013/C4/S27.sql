SELECT
  __g2 AS "Task Type",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 1) AS "avg_planned",
  ROUND((
    1.0 * SUM(__a14_sum) / NULLIF(SUM(__a14_n), 0)
  ), 1) AS "avg_actual",
  ROUND((
    1.0 * SUM(__a15_sum) / NULLIF(SUM(__a15_n), 0)
  ), 2) AS "avg_quality"
FROM temp."reuse_013_c4"
GROUP BY
  __g2
ORDER BY
  __g2;
