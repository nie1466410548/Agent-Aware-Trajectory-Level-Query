SELECT 
  SUM(CASE WHEN candidate_hire_rate IS NULL THEN 1 ELSE 0 END) AS null_hire_rate,
  SUM(CASE WHEN avg_total_days_to_hire IS NULL THEN 1 ELSE 0 END) AS null_days,
  SUM(CASE WHEN avg_candidate_experience_score IS NULL THEN 1 ELSE 0 END) AS null_exp,
  SUM(CASE WHEN feedback_completion_rate_managed IS NULL THEN 1 ELSE 0 END) AS null_feedback,
  SUM(CASE WHEN total_requisitions_owned IS NULL THEN 1 ELSE 0 END) AS null_req
FROM lever__hiring_manager_scorecard