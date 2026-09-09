SELECT
  __g0 AS "Video Category",
  SUM(__a0) AS "total_videos",
  SUM(__a28) AS "top10_count",
  ROUND(100.0 * SUM(__a28) / SUM(__a0), 1) AS "top10_pct",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score"
FROM temp."reuse_014_c2"
GROUP BY
  __g0
HAVING
  SUM(__a0) >= 15
ORDER BY
  top10_pct DESC
LIMIT 20;
