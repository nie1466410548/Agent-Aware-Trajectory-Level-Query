-- Difficulty mix by year (share of levels)
SELECT strftime('%Y', "Launch Time") as yr, "Difficulty Level", COUNT(*) as cnt
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") IN ('2022','2023','2024')
GROUP BY yr, "Difficulty Level"
ORDER BY yr, cnt DESC