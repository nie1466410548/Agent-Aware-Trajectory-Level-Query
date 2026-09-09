SELECT
  __g3 AS "Task Owner",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 3) AS "avg_diff"
FROM temp."reuse_013_c4"
GROUP BY
  __g3;
