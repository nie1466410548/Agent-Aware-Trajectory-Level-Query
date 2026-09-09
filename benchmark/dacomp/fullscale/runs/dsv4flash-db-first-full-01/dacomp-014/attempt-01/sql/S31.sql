SELECT 
  CASE 
    WHEN "Creator Followers" < 10000 THEN '1. <10k'
    WHEN "Creator Followers" < 100000 THEN '2. 10k-100k'
    WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M'
    ELSE '4. >1M' 
  END as follower_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Coins")) as avg_coins
FROM sheet1
GROUP BY follower_band
ORDER BY follower_band