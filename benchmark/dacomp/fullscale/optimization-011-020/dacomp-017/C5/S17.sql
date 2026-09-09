SELECT
  __g0 AS "Discount",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 4) AS "avg_margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g0
ORDER BY
  __g0;
