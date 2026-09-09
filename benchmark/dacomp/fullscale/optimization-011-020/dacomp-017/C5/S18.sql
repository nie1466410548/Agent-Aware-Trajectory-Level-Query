SELECT
  __g1 AS "Shipping Method",
  SUM(__a0) AS "n",
  SUM(__a2) AS "total_profit",
  SUM(__a3) AS "total_sales",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 4) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g1
ORDER BY
  __g1;
