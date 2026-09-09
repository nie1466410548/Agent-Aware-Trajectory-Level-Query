WITH score_components AS (
  SELECT
    hiring_manager_id,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
)
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END) AS days_met,
  SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END) AS exp_met,
  SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END) AS feedback_met,
  SUM(CASE WHEN hire_rate_score >= 50 THEN 1 ELSE 0 END) AS hire_rate_ge50,
  SUM(CASE WHEN days_score = 100 AND experience_score = 100 AND feedback_score = 100 AND hire_rate_score >= 50 THEN 1 ELSE 0 END) AS all_four_strong,
  ROUND(AVG(hire_rate_score), 2) AS avg_hire_rate_score
FROM score_components