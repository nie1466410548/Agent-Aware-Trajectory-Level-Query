SELECT team_id, total_tasks, completed_tasks, completion_rate, avg_project_health,
avg_hours_atc, n_users
FROM (
  SELECT team_id, COUNT(*) AS total_tasks,
  SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
  ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  ROUND(AVG(project_health_score),2) AS avg_project_health,
  ROUND(AVG(hours_assigned_to_completion),1) AS avg_hours_atc,
  COUNT(DISTINCT assignee_user_id) AS n_users
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1
  GROUP BY team_id
)
ORDER BY completion_rate DESC