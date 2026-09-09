SELECT 
  "Creator Video Count",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares
FROM sheet1
GROUP BY "Creator Video Count"
ORDER BY "Creator Video Count" DESC
LIMIT 20