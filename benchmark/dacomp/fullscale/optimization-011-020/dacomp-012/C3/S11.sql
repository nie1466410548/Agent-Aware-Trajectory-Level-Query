SELECT
  MIN(__a14) AS "min_carat",
  MAX(__a15) AS "max_carat",
  MIN(__a11) AS "min_price",
  MAX(__a12) AS "max_price",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ), 3) AS "avg_carat",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ), 2) AS "avg_price",
  ROUND((
    1.0 * SUM(__a17_sum) / NULLIF(SUM(__a17_n), 0)
  ), 2) AS "avg_ppc",
  ROUND((
    1.0 * SUM(__a18_sum) / NULLIF(SUM(__a18_n), 0)
  ), 2) AS "avg_depth",
  ROUND((
    1.0 * SUM(__a19_sum) / NULLIF(SUM(__a19_n), 0)
  ), 2) AS "avg_table"
FROM temp."reuse_012_c3";
