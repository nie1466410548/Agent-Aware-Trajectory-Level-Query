SELECT
  __g1 AS "Color",
  SUM(__a0) AS "n"
FROM temp."reuse_012_c3"
GROUP BY
  __g1
ORDER BY
  __g1;
