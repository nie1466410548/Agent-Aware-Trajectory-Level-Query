SELECT 
  COUNT(*) as n,
  SUM(CASE WHEN days_span - active_days >= 90 THEN 1 ELSE 0 END) as inactive_90plus,
  SUM(CASE WHEN days_span - active_days >= 60 THEN 1 ELSE 0 END) as inactive_60plus,
  SUM(CASE WHEN days_span - active_days >= 30 THEN 1 ELSE 0 END) as inactive_30plus,
  AVG(days_span - active_days) as avg_inactive_days
FROM klaviyo__persons