SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
ORDER BY avg_views DESC
LIMIT 20