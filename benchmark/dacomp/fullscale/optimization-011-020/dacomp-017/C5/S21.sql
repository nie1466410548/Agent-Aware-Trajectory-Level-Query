SELECT
  __g3 AS "Product",
  SUM(__a0) AS "n",
  SUM(__a3) AS "total_sales",
  SUM(__a2) AS "total_profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 6) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3
ORDER BY
  margin;
