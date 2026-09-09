SELECT j.created_year, j.created_month,
  COUNT(DISTINCT j.job_id) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  SUM(j.count_completed_interviews) AS interviews,
  ROUND(100.0*SUM(j.count_completed_interviews)/SUM(j.count_total_applications),2) AS weighted_interview_rate,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_job_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.created_year, j.created_month
ORDER BY j.created_year, j.created_month