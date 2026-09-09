
SELECT j.hiring_managers, j.departments,
  COUNT(DISTINCT j.name) AS distinct_roles,
  COUNT(DISTINCT j.created_month) AS months_active,
  COUNT(*) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers
ORDER BY avg_rate
