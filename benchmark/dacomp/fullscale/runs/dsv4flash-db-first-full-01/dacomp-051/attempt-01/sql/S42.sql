
SELECT CAST(t.assignee_user_id AS TEXT) AS user_id, u.user_name,
  u.avg_close_time_assigned_days,
  u.number_of_open_tasks,
  u.number_of_tasks_completed,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_activity_rate,
  SUM(CASE WHEN t.delay_days>0 THEN 1 ELSE 0 END) AS n_delayed
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.assignee_user_id
