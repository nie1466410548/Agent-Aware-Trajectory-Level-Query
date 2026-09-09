SELECT t.complexity_execution_match, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.complexity_execution_match
ORDER BY cnt DESC