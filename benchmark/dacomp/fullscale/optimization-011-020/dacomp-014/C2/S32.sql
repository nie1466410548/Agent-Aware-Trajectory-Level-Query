SELECT
  __g10 AS "video_count_band",
  SUM(__a0) AS "cnt",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank"
FROM temp."reuse_014_c2"
GROUP BY
  __g10
ORDER BY
  video_count_band;
