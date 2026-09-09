SELECT t.team_id,
  COUNT(*) FILTER (WHERE is_completed=1) AS completed_cnt,
  COUNT(*) AS total_cnt,
  ROUND(100.0*COUNT(*) FILTER (WHERE is_completed=1)/COUNT(*),1) AS completion_rate,
  COUNT(DISTINCT CAST(t.assignee_user_id AS TEXT)) AS n_users,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN CAST(t.assignee_user_id AS TEXT) END) AS n_slow_users,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc_hours
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
HAVING total_cnt >= 50
ORDER BY completion_rate ASC
LIMIT 15