SELECT 
  ROUND(CORR("Churn Rate", "Level Rating"), 4) as corr_churn_rating,
  ROUND(CORR("Churn Rate", "Clear Rate"), 4) as corr_churn_clear,
  ROUND(CORR("Level Rating", "Clear Rate"), 4) as corr_rating_clear,
  ROUND(CORR("Churn Rate", "Average Retry Count"), 4) as corr_churn_retry
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'