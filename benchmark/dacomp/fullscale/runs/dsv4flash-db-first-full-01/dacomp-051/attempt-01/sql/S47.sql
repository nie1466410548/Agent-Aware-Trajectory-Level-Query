SELECT t.project_name,
  COUNT(*) AS n_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS completion_rate,
  ROUND(AVG(t.project_health_score),1) AS avg_project_health,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.project_name
ORDER BY n_tasks DESC
LIMIT 15