
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS comp_rate
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1 AND created_at IS NOT NULL
GROUP BY month ORDER BY month
