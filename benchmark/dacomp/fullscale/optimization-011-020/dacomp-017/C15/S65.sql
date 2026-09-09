SELECT
  __g0 AS "yr",
  (
    1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)
  ) AS "avg_discount",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_qty_discount"
FROM temp."reuse_017_c15"
GROUP BY
  __g0
ORDER BY
  yr;
