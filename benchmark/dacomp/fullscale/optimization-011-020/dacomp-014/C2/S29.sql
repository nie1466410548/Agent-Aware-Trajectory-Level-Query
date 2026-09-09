SELECT
  __g8 AS "Creator",
  SUM(__a0) AS "num_videos_in_ranking",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers",
  ROUND((
    1.0 * SUM(__a27_sum) / NULLIF(SUM(__a27_n), 0)
  )) AS "avg_video_count"
FROM temp."reuse_014_c2"
GROUP BY
  __g8
HAVING
  SUM(__a0) >= 10
ORDER BY
  avg_rank ASC
LIMIT 20;
