SELECT 
  "Main Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / 520, 1) as top10_pct,
  SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) as top30_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) / 1560, 1) as top30_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Main Category"
ORDER BY top10_count DESC