SELECT r.application_quarter, j.departments,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  ROUND(100.0*SUM(r.total_interviews)/SUM(r.total_applications),2) AS app_to_interview_pct,
  ROUND(100.0*SUM(r.hired_count)/SUM(r.total_applications),2) AS hire_pct
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
GROUP BY r.application_quarter, j.departments
ORDER BY r.application_quarter, j.departments