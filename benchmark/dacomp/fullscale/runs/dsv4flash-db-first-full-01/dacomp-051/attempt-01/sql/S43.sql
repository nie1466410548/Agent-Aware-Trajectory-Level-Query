
SELECT t.team_id,
  COUNT(*) AS total_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
