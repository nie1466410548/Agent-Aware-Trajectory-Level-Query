WITH slow_users AS (
  SELECT user_id FROM asana__user
  WHERE avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
)
SELECT
  CASE WHEN s.user_id IS NOT NULL THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_users,
  ROUND(AVG(u.number_of_open_tasks),2) AS avg_open_tasks,
  ROUND(AVG(u.number_of_tasks_completed),2) AS avg_completed_tasks,
  ROUND(AVG(u.avg_close_time_assigned_days),2) AS avg_close_time_assigned
FROM asana__user u
LEFT JOIN slow_users s ON u.user_id = s.user_id
GROUP BY cohort