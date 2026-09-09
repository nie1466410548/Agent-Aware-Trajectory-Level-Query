SELECT
  MIN(__a3) AS "min_views",
  (
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ) AS "avg_views",
  MAX(__a5) AS "max_views",
  MIN(__a6) AS "min_likes",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_likes",
  MAX(__a8) AS "max_likes",
  MIN(__a9) AS "min_coins",
  (
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  ) AS "avg_coins",
  MAX(__a11) AS "max_coins",
  MIN(__a12) AS "min_fav",
  (
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ) AS "avg_fav",
  MAX(__a14) AS "max_fav",
  MIN(__a15) AS "min_shares",
  (
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ) AS "avg_shares",
  MAX(__a17) AS "max_shares",
  MIN(__a18) AS "min_comments",
  (
    1.0 * SUM(__a19_sum) / NULLIF(SUM(__a19_n), 0)
  ) AS "avg_comments",
  MAX(__a20) AS "max_comments",
  MIN(__a21) AS "min_danmaku",
  (
    1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
  ) AS "avg_danmaku",
  MAX(__a23) AS "max_danmaku"
FROM temp."reuse_014_c2";
