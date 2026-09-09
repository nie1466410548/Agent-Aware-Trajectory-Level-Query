SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS tasks_created,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS completion_rate,
ROUND(AVG(complexity_score),2) AS avg_complexity,
ROUND(AVG(project_health_score),2) AS avg_health
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1
GROUP BY month ORDER BY month