SELECT
  __g0 AS "Customer ID",
  SUM(__a0) AS "cnt"
FROM temp."reuse_018_c7"
GROUP BY
  __g0
ORDER BY
  cnt DESC
LIMIT 10;
