SELECT COUNT(*) AS eligible, 
  MIN(candidate_hire_rate) AS min_hr, MAX(candidate_hire_rate) AS max_hr,
  MIN(avg_total_days_to_hire) AS min_days, MAX(avg_total_days_to_hire) AS max_days,
  MIN(avg_candidate_experience_score) AS min_exp, MAX(avg_candidate_experience_score) AS max_exp,
  MIN(feedback_completion_rate_managed) AS min_fb, MAX(feedback_completion_rate_managed) AS max_fb,
  MIN(total_requisitions_owned) AS min_req, MAX(total_requisitions_owned) AS max_req
FROM lever__hiring_manager_scorecard
WHERE total_requisitions_owned >= 5