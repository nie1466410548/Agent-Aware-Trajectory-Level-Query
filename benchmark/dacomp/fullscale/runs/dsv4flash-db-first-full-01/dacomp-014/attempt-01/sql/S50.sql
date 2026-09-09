SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as vstatus,
  COUNT(*) as cnt,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_2m,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_1m,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY vstatus