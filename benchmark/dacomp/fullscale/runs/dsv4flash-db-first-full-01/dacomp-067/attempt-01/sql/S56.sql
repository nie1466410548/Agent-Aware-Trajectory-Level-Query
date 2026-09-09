SELECT current_job_stage, COUNT(*) as cnt,
       AVG(julianday(last_activity_at) - julianday(applied_at)) as avg_days_in_process
FROM greenhouse__application_enhanced
WHERE last_activity_at IS NOT NULL AND applied_at IS NOT NULL
GROUP BY current_job_stage
ORDER BY avg_days_in_process