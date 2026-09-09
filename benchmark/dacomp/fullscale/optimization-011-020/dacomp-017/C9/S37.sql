SELECT
  __g0 AS "Quantity",
  SUM(__a0) AS "n",
  SUM(__a1) AS "profit",
  SUM(__a2) AS "sales",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "margin"
FROM temp."reuse_017_c9"
GROUP BY
  __g0
ORDER BY
  __g0;
