SELECT "Difficulty Level", COUNT(*) as cnt, ROUND(AVG("Churn Rate"),4) as avg_churn, ROUND(AVG("Level Rating"),4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level" ORDER BY avg_churn DESC