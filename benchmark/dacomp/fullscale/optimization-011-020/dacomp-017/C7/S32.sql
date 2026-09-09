SELECT
  __g0 AS "Quantity",
  __g1 AS "Discount",
  SUM(__a0) AS "n",
  SUM(__a1) AS "sales",
  SUM(__a2) AS "profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a1), 4) AS "margin"
FROM temp."reuse_017_c7"
GROUP BY
  __g0,
  __g1
ORDER BY
  __g0,
  __g1;
