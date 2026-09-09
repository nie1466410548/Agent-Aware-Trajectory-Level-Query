SELECT
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND(MIN(__a2), 2) AS "min_exam",
  ROUND(MAX(__a3), 2) AS "max_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study",
  ROUND((
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ), 2) AS "avg_social",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 2) AS "avg_attendance",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 2) AS "avg_sleep",
  ROUND((
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ), 2) AS "avg_exercise",
  ROUND((
    1.0 * SUM(__a9_sum) / NULLIF(SUM(__a9_n), 0)
  ), 2) AS "avg_mh"
FROM temp."reuse_011_c2";
