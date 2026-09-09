-- Yearly trend of churn and rating by difficulty to check stability
SELECT strftime('%Y', "Launch Time") as yr, "Difficulty Level",
  COUNT(*) as cnt, ROUND(AVG("Churn Rate"), 4) as avg_churn, ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") IN ('2022','2023','2024')
GROUP BY yr, "Difficulty Level"
ORDER BY yr, avg_churn DESC