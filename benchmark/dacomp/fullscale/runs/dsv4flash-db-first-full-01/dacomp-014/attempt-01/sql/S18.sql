SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate,
  ROUND(1.0*AVG("Comments")/AVG("Views")*100, 2) as comment_rate,
  ROUND(1.0*AVG("Danmaku Count")/AVG("Views")*100, 2) as danmaku_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY like_rate DESC
LIMIT 20