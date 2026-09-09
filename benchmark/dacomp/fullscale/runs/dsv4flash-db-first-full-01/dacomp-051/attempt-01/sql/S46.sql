SELECT t.success_patterns, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days <= (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.success_patterns
ORDER BY cnt DESC