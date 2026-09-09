SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a2) * 1.0 / SUM(__a3) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  yr;
