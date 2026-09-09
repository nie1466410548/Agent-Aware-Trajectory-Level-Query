SELECT 
  "Difficulty Level",
  "Level Type",
  COUNT(*) as level_count,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating,
  ROUND(AVG("Clear Rate"), 4) as avg_clear_rate,
  ROUND(AVG("Average Retry Count"), 2) as avg_retries
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level", "Level Type"
ORDER BY "Difficulty Level", "Level Type"