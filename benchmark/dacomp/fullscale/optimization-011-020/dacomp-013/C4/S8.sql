SELECT
  __g3 AS "Task Owner",
  SUM(__a0) AS "cnt"
FROM temp."reuse_013_c4"
GROUP BY
  __g3
ORDER BY
  cnt DESC;
