SELECT
  __g0 AS "Discount",
  __g2 AS "yr",
  SUM(__a0) AS "n",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_margin",
  (
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ) AS "avg_profit",
  (
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ) AS "avg_sales"
FROM temp."reuse_017_c5"
GROUP BY
  __g0,
  __g2
ORDER BY
  __g0,
  yr;
