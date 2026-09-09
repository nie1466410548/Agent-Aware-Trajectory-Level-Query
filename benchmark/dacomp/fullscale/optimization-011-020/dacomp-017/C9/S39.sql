SELECT
  __g1 AS "yr",
  __g0 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c9"
GROUP BY
  __g1,
  __g0
ORDER BY
  yr,
  __g0;
