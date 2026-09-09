SELECT hiring_managers,
  MIN(created_month) AS first_month,
  MAX(created_month) AS last_month,
  COUNT(DISTINCT created_month) AS months_active,
  COUNT(DISTINCT name) AS distinct_job_titles,
  COUNT(*) AS n_jobs,
  SUM(count_total_applications) AS total_apps
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
GROUP BY hiring_managers
ORDER BY hiring_managers