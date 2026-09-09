SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 5
ORDER BY avg_views DESC
LIMIT 20