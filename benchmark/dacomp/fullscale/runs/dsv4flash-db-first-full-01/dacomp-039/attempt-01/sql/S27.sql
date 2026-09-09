SELECT MIN("Level Completion Rate" + "Churn Rate") as min_sum,
       MAX("Level Completion Rate" + "Churn Rate") as max_sum,
       ROUND(AVG("Level Completion Rate" + "Churn Rate"), 4) as avg_sum
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'