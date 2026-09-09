
SELECT t.team_id,
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  ROUND(AVG(t.project_health_score),2) AS avg_project_health,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_hours_atc,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  COUNT(DISTINCT t.assignee_user_id) AS n_users,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users,
  ROUND(100.0*COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)/NULLIF(COUNT(DISTINCT t.assignee_user_id),0),2) AS slow_user_pct
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
ORDER BY completion_rate ASC
