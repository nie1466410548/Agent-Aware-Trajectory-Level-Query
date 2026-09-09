-- Cross-tab Difficulty x Reward Type for 2024
SELECT "Difficulty Level", "Reward Type", COUNT(*) as cnt
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level", "Reward Type"
ORDER BY "Difficulty Level", cnt DESC