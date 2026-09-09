SELECT
  __g1 AS "Priority",
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  __g0;
