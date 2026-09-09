SELECT 
  "Main Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY "Main Category"
ORDER BY avg_views DESC