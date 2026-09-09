SELECT
  __g1 AS "alert",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c3"
GROUP BY
  __g1;
