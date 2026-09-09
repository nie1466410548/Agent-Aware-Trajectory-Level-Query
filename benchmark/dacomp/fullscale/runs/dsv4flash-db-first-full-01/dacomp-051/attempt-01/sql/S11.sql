SELECT
  COUNT(*) AS slow_tasks,
  SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS slow_completed,
  ROUND(AVG(complexity_score),3) AS avg_complexity,
  ROUND(AVG(urgency_score),3) AS avg_urgency,
  ROUND(AVG(project_health_score),3) AS avg_project_health,
  ROUND(AVG(hours_assigned_to_completion),2) AS avg_hours_atc,
  ROUND(AVG(avg_daily_activity_rate),4) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)