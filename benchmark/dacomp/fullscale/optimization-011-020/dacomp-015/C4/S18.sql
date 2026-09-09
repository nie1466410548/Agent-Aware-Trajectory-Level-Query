SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "watch_gt0",
  SUM(__a2) AS "watch_eq0",
  SUM(__a3) AS "watch_gt50",
  SUM(__a4) AS "show_gt0",
  SUM(__a5) AS "show_eq0",
  SUM(__a6) AS "show_gt10",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_watch",
  (
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ) AS "avg_show",
  MAX(__a9) AS "max_watch",
  MAX(__a10) AS "max_show",
  MIN(__a11) AS "min_watch",
  MIN(__a12) AS "min_show"
FROM temp."reuse_015_c4";
