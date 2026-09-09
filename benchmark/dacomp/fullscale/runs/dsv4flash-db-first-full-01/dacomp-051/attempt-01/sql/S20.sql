SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS tasks,
  ROUND(AVG(t.hours_to_assignment),2) AS avg_hours_to_assign,
  ROUND(AVG(t.hours_assigned_to_completion),2) AS avg_hours_atc,
  ROUND(AVG(t.total_lifecycle_hours),2) AS avg_lifecycle_hours,
  ROUND(AVG(t.total_story_events),2) AS avg_story_events,
  ROUND(AVG(t.unique_action_types),2) AS avg_action_types,
  ROUND(AVG(t.days_with_activity),2) AS avg_activity_days,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_daily_activity_rate,
  ROUND(AVG(t.delay_days),2) AS avg_delay_days,
  ROUND(AVG(t.response_time_days),2) AS avg_response_days
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort