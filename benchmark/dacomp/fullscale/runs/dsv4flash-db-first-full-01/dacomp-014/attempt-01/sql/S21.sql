SELECT 
  ROUND(AVG("Overall Score")) as avg_overall_score,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Total Views")) as avg_creator_views,
  ROUND(AVG("Creator Total Likes")) as avg_creator_likes,
  ROUND(AVG("Creator Video Count")) as avg_creator_videos
FROM sheet1
WHERE "Rank" <= 10