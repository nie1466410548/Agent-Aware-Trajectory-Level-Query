SELECT
  __g3 AS "verification_status",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers"
FROM temp."reuse_014_c2"
GROUP BY
  __g3;
