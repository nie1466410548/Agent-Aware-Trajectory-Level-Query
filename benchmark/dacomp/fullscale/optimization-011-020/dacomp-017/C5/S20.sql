SELECT
  __g2 AS "yr",
  __g0 AS "Discount",
  SUM(__a0) AS "n",
  ROUND(SUM(__a2), 1) AS "total_profit",
  ROUND(SUM(__a3), 1) AS "total_sales",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 6) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;
