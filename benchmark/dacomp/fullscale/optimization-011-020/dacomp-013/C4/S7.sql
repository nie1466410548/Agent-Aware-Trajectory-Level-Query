SELECT
  __g2 AS "Task Type",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g2;
