SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 10
ORDER BY avg_rank ASC
LIMIT 20