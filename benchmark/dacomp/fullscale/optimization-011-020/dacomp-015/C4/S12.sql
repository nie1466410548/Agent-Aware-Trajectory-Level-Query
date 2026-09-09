SELECT
  __g3 AS "Orientation",
  SUM(__a0) AS "cnt"
FROM temp."reuse_015_c4"
GROUP BY
  __g3
ORDER BY
  cnt DESC;
