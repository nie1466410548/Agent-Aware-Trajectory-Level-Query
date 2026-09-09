SELECT
  __g2 AS "Task Type",
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g2,
  __g0
ORDER BY
  __g2,
  __g0;
