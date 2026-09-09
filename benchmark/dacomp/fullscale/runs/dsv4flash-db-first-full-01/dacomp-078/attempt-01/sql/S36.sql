-- Detailed distribution of last_event_on by month
SELECT substr(last_event_on,1,7) AS last_month, COUNT(*) AS accounts,
  AVG(sum_minutes) AS avg_min, AVG(sum_events) AS avg_events,
  AVG(count_active_days) AS avg_days,
  AVG(count_active_months) AS avg_months
FROM pendo__account
GROUP BY last_month
ORDER BY last_month