-- Stat summary by difficulty for 2024
SELECT 
  "Difficulty Level",
  COUNT(*) as cnt,
  ROUND(MIN("Churn Rate"), 4) as min_churn,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(MAX("Churn Rate"), 4) as max_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating,
  ROUND(AVG("Clear Rate"), 4) as avg_clear,
  ROUND(AVG("Average Retry Count"), 2) as avg_retries,
  ROUND(AVG("Level Completion Rate"), 4) as avg_completion
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level"
ORDER BY avg_churn DESC