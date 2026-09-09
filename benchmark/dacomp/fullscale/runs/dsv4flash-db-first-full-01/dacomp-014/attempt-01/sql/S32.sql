SELECT 
  CASE 
    WHEN "Creator Video Count" = 100 THEN '100 (full)'
    WHEN "Creator Video Count" < 10 THEN '1-9'
    WHEN "Creator Video Count" < 50 THEN '10-49'
    ELSE '50-99'
  END as video_count_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY video_count_band
ORDER BY video_count_band