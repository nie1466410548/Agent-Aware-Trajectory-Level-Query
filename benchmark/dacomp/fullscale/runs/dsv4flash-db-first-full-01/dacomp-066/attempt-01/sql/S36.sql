
SELECT j.created_month,
  COUNT(DISTINCT j.job_id) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  SUM(j.count_completed_interviews) AS interviews,
  100.0*SUM(j.count_completed_interviews)/SUM(j.count_total_applications) AS interview_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.created_month
ORDER BY j.created_month
