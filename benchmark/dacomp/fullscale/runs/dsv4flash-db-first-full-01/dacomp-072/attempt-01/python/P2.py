import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Retrieve the full composite scorecard via logged interface
res = db.query("""
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned,
       hire_rate_score, days_score, experience_score, feedback_score, composite_score
FROM composite
ORDER BY composite_score DESC
""")
df = db.frame(res)
print(df.shape)
print(df.head())
df.to_json('/work/full_scorecard.json', orient='records', lines=True)