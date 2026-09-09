SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a0) AS "n",
  ROUND(SUM(__a3), 0) AS "total_sales",
  ROUND(SUM(__a2), 1) AS "total_profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 4) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  yr;
