WITH score_components AS (
  SELECT
    hiring_manager_id,
    total_requisitions_owned,
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
SELECT 
  CASE WHEN total_requisitions_owned BETWEEN 5 AND 19 THEN '5-19'
       WHEN total_requisitions_owned BETWEEN 20 AND 39 THEN '20-39'
       ELSE '40+' END AS req_bucket,
  COUNT(*) AS n,
  ROUND(AVG(composite_score), 2) AS avg_score,
  ROUND(AVG(hire_rate_score), 2) AS avg_hire_rate
FROM composite
GROUP BY req_bucket
ORDER BY req_bucket