
SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter
