SELECT 
  "Video Category",
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Favorites")) as avg_fav,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku
FROM sheet1
WHERE "Main Category" = 'Whole site'
GROUP BY "Video Category"
HAVING COUNT(*) >= 3
ORDER BY avg_views DESC
LIMIT 15