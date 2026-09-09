SELECT
  __g2 AS "yr",
  __g0 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c7"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;
