SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as verification_status,
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers
FROM sheet1
GROUP BY verification_status