SELECT
  __g1 AS "Main Category",
  SUM(__a0) AS "total_videos",
  SUM(__a28) AS "top10_count",
  ROUND(100.0 * SUM(__a28) / 520, 1) AS "top10_pct",
  SUM(__a29) AS "top30_count",
  ROUND(100.0 * SUM(__a29) / 1560, 1) AS "top30_pct",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score"
FROM temp."reuse_014_c2"
GROUP BY
  __g1
ORDER BY
  top10_count DESC;
