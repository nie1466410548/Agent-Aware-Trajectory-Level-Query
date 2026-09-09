-- Visitor-level features per account: browser and OS diversity
SELECT 
  v.account_id,
  COUNT(DISTINCT v.last_browser_name) AS browser_diversity,
  COUNT(DISTINCT v.last_operating_system) AS os_diversity,
  AVG(v.sum_minutes) AS avg_visitor_minutes,
  AVG(v.sum_events) AS avg_visitor_events,
  STDDEV(v.sum_minutes) AS std_visitor_minutes,
  STDDEV(v.sum_events) AS std_visitor_events,
  AVG(v.average_daily_minutes) AS avg_visitor_daily_min,
  AVG(v.average_daily_events) AS avg_visitor_daily_events,
  AVG(v.count_active_days) AS avg_visitor_active_days
FROM pendo__visitor v
GROUP BY v.account_id
LIMIT 10