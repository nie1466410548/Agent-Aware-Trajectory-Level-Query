SELECT COUNT(*) AS user_count, ROUND(AVG(avg_close_time_assigned_days),4) AS overall_avg,
ROUND(1.5*AVG(avg_close_time_assigned_days),4) AS threshold_15x,
MIN(avg_close_time_assigned_days) AS min_val, MAX(avg_close_time_assigned_days) AS max_val
FROM asana__user