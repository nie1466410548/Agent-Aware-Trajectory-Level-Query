WITH user_task_stats AS (
  SELECT CAST(assignee_user_id AS TEXT) AS user_id,
    COUNT(*) AS n_tasks,
    SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
    ROUND(AVG(complexity_score),2) AS avg_task_complexity,
    ROUND(AVG(urgency_score),2) AS avg_task_urgency,
    ROUND(AVG(project_health_score),2) AS avg_project_health
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1 AND assignee_user_id IS NOT NULL
  GROUP BY assignee_user_id
)
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_matched_users,
  ROUND(AVG(ts.n_tasks),2) AS avg_tasks_per_user,
  ROUND(AVG(ts.avg_task_complexity),2) AS avg_task_complexity,
  ROUND(AVG(ts.avg_task_urgency),2) AS avg_task_urgency,
  ROUND(AVG(ts.avg_project_health),2) AS avg_proj_health
FROM asana__user u
JOIN user_task_stats ts ON u.user_id = ts.user_id
GROUP BY cohort