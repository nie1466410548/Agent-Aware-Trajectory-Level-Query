SELECT
  __g2 AS "yr",
  __g5 AS "Order Priority",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g5
ORDER BY
  yr,
  __g5;
