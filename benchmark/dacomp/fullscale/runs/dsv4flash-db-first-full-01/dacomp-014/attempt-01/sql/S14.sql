SELECT 
  "Creator Gender",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator Gender"