SELECT ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS overall_completion_rate,
ROUND(AVG(project_health_score),2) AS overall_avg_health,
ROUND(AVG(complexity_score),2) AS overall_avg_complexity,
ROUND(AVG(urgency_score),2) AS overall_avg_urgency
FROM asana__task_lifecycle_analysis WHERE is_valid_record=1