-- Number of daily metric rows per account
SELECT v.account_id, COUNT(*) AS dm_rows, COUNT(DISTINCT dm.visitor_id) AS dm_visitors,
       MIN(dm.date_day) AS min_day, MAX(dm.date_day) AS max_day
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id
ORDER BY dm_rows DESC