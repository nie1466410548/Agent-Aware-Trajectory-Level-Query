SELECT 
  "Video Category",
  COUNT(*) as cnt,
  ROUND(100.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_viral_2m,
  ROUND(AVG("Views")) as avg_views
FROM sheet1
GROUP BY "Video Category"
HAVING cnt >= 15
ORDER BY pct_viral_2m DESC
LIMIT 15