
SELECT u.user_id, u.user_name, u.avg_close_time_assigned_days,
  u.number_of_open_tasks, u.number_of_tasks_completed,
  ts.n_tasks AS tasks_in_table,
  ts.n_completed AS completed_in_table
FROM asana__user u
LEFT JOIN (
  SELECT CAST(assignee_user_id AS TEXT) AS user_id, COUNT(*) AS n_tasks,
    SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1
  GROUP BY assignee_user_id
) ts ON u.user_id = ts.user_id
