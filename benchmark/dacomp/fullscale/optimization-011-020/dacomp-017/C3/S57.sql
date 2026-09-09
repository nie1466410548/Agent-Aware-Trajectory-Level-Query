SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a1) * 1.0 / SUM(__a2) AS "margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;
