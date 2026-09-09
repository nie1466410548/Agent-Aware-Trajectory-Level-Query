SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  ROUND(100.0*SUM(r.total_interviews)/SUM(r.total_applications),2) AS interview_rate,
  SUM(r.hired_count) AS hired,
  ROUND(100.0*SUM(r.hired_count)/SUM(r.total_applications),2) AS hire_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter