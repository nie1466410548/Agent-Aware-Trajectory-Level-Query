-- Same combination analysis for ALL years (context for 2024 patterns)
SELECT 
  "Difficulty Level", "Level Type", COUNT(*) as cnt,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
GROUP BY "Difficulty Level", "Level Type"
ORDER BY avg_churn DESC