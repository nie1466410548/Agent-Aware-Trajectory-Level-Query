-- Correlation proxy: reward value ranges by difficulty
SELECT "Difficulty Level", MIN("Reward Value") as min_rw, MAX("Reward Value") as max_rw, ROUND(AVG("Reward Value"),2) as avg_rw
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level" ORDER BY avg_rw DESC