SELECT u.user_id, u.user_name, u.avg_close_time_assigned_days,
u.number_of_open_tasks, u.number_of_tasks_completed
FROM asana__user u
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
ORDER BY u.avg_close_time_assigned_days DESC
LIMIT 30