SELECT urgency_score, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),2) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY urgency_score ORDER BY urgency_score