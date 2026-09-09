SELECT hiring_managers, COUNT(*) AS n_jobs,
  SUM(count_total_applications) AS apps,
  SUM(count_completed_interviews) AS interviews,
  ROUND(100.0*SUM(count_completed_interviews)/SUM(count_total_applications),2) AS weighted_rate
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
GROUP BY hiring_managers
ORDER BY weighted_rate