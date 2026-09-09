SELECT
  __g0 AS "Floor Plan",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g0
ORDER BY
  cnt DESC;
