SELECT
  __g4 AS "Watch Count",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g4
ORDER BY
  __g4 DESC
LIMIT 20;
