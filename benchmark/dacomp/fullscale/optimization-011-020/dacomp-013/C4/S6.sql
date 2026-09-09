SELECT
  __g1 AS "Priority",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g1;
