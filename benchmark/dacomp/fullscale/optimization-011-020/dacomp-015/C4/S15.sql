SELECT
  __g1 AS "Floor",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g1
ORDER BY
  __g1;
