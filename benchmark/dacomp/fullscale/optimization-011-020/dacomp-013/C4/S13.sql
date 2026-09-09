SELECT
  MIN(__a5) AS "min_planned",
  MAX(__a6) AS "max_planned",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_planned",
  SUM(__a8) AS "missing_actual_hours",
  SUM(__a9) AS "missing_quality",
  SUM(__a10) AS "missing_rework"
FROM temp."reuse_013_c4";
