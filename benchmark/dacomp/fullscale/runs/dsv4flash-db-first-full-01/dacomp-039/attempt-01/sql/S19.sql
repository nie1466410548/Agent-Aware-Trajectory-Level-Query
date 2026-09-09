-- Deviation of each Difficulty x Type combo from its Difficulty baseline (2024)
WITH base AS (
  SELECT "Difficulty Level", AVG("Churn Rate") AS d_churn, AVG("Level Rating") AS d_rating
  FROM game_game_level_content_data_ta
  WHERE strftime('%Y', "Launch Time") = '2024'
  GROUP BY "Difficulty Level"
),
comb AS (
  SELECT "Difficulty Level", "Level Type", COUNT(*) as cnt,
    AVG("Churn Rate") as c_churn, AVG("Level Rating") as c_rating
  FROM game_game_level_content_data_ta
  WHERE strftime('%Y', "Launch Time") = '2024'
  GROUP BY "Difficulty Level", "Level Type"
)
SELECT comb."Difficulty Level", comb."Level Type", comb.cnt,
  ROUND(comb.c_churn, 4) as combo_churn, ROUND(base.d_churn, 4) as diff_avg_churn,
  ROUND(comb.c_churn - base.d_churn, 4) as churn_dev,
  ROUND(comb.c_rating, 2) as combo_rating, ROUND(base.d_rating, 2) as diff_avg_rating,
  ROUND(comb.c_rating - base.d_rating, 2) as rating_dev
FROM comb JOIN base ON comb."Difficulty Level" = base."Difficulty Level"
ORDER BY churn_dev DESC