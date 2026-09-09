SELECT
  __g0 AS "Task Status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g0;
