SELECT 
  CASE WHEN "Rank" <= 10 THEN 'Top 10'
       WHEN "Rank" <= 30 THEN '11-30'
       WHEN "Rank" <= 50 THEN '31-50'
       WHEN "Rank" <= 70 THEN '51-70'
       ELSE '71-100' END as rank_band,
  "Main Category",
  COUNT(*) as count
FROM sheet1
GROUP BY rank_band, "Main Category"
ORDER BY rank_band, count DESC