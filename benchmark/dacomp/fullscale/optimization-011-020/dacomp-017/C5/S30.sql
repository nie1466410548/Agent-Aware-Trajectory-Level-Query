SELECT
  __g2 AS "yr",
  __g4 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g4
ORDER BY
  yr,
  __g4;
