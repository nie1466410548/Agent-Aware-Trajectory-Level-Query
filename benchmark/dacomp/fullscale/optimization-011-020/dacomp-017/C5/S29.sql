SELECT
  __g2 AS "yr",
  __g0 AS "Discount",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;
