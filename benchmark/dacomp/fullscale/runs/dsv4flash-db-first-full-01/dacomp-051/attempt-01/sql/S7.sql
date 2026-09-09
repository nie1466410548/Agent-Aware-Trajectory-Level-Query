SELECT COUNT(*) AS slow_user_count FROM asana__user
WHERE avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)