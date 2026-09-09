SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a4) AS "neg_rows",
  SUM(__a0) AS "n",
  SUM(__a5) AS "neg_profit"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;
