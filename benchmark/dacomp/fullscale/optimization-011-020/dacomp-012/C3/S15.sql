SELECT
  __g2 AS "Clarity",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat"
FROM temp."reuse_012_c3"
GROUP BY
  __g2
ORDER BY
  __g2;
