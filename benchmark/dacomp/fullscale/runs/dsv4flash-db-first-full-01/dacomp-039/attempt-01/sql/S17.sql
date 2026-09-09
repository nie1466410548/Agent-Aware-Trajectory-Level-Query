-- Monthly trends in 2024
SELECT 
  strftime('%Y-%m', "Launch Time") as launch_month,
  COUNT(*) as level_count,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY launch_month
ORDER BY launch_month