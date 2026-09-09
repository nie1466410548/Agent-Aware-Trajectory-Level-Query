
SELECT v.account_id,
       substr(dm.date_day, 1, 7) AS month,
       SUM(dm.sum_minutes) AS month_minutes,
       SUM(dm.sum_events) AS month_events,
       COUNT(DISTINCT dm.visitor_id) AS month_visitors,
       COUNT(DISTINCT dm.date_day) AS month_active_days
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id, substr(dm.date_day, 1, 7)
ORDER BY v.account_id, month
