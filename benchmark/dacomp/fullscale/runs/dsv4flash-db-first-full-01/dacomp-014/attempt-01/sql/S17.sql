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
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY avg_views DESC
LIMIT 20