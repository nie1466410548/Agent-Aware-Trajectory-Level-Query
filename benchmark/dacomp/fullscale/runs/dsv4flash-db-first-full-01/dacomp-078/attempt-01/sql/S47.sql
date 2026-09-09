
SELECT v.account_id,
  COUNT(DISTINCT v.last_browser_name) AS browser_diversity,
  COUNT(DISTINCT v.last_operating_system) AS os_diversity,
  AVG(v.sum_minutes) AS avg_visitor_minutes,
  AVG(v.sum_events) AS avg_visitor_events,
  AVG(v.average_daily_minutes) AS avg_visitor_daily_min,
  AVG(v.average_daily_events) AS avg_visitor_daily_events,
  AVG(v.count_active_days) AS avg_visitor_active_days,
  AVG(v.count_active_months) AS avg_visitor_active_months,
  SUM(v.sum_minutes) AS total_visitor_minutes,
  SUM(v.sum_events) AS total_visitor_events
FROM pendo__visitor v
GROUP BY v.account_id
ORDER BY v.account_id
