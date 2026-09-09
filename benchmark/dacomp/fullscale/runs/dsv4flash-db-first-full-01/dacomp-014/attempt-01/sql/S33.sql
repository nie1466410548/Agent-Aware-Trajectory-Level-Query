SELECT 
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_5m,
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_2m
FROM sheet1