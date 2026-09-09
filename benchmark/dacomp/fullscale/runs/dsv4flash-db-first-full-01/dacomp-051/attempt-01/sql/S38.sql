
SELECT strftime('%Y-%m', t.created_at) AS month,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1 AND t.created_at IS NOT NULL
GROUP BY month, cohort
ORDER BY month
