SELECT
  __g3 AS "transport",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c2"
GROUP BY
  __g3;
