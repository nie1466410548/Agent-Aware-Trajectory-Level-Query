SELECT
  MIN(__a11) AS "min_diff",
  MAX(__a12) AS "max_diff",
  (
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ) AS "avg_diff"
FROM temp."reuse_013_c4";
