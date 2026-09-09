-- NOT APPROVED: result comparison failed. Use the original SQL for this query.
SELECT
  MIN(__a1) AS "min_mh",
  MAX(__a2) AS "max_mh",
  (
    1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)
  ) AS "avg_mh",
  MIN(__a4) AS "min_exam",
  MAX(__a5) AS "max_exam",
  (
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ) AS "avg_exam"
FROM temp."reuse_020_c2";
