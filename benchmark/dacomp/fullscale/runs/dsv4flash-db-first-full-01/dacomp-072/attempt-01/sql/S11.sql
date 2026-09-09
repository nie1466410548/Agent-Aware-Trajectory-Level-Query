WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    hiring_manager_email,
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
SELECT ROUND(MIN(composite_score),2) AS min_score,
       ROUND(MAX(composite_score),2) AS max_score,
       ROUND(AVG(composite_score),2) AS mean_score,
       ROUND(AVG(composite_score*composite_score) - AVG(composite_score)*AVG(composite_score), 2) AS variance,
       COUNT(*) AS total_managers
FROM composite