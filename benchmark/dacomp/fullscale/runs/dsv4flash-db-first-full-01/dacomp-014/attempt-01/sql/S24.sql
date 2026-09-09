SELECT 
  "Video Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / COUNT(*), 1) as top10_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
HAVING COUNT(*) >= 15
ORDER BY top10_pct DESC
LIMIT 20