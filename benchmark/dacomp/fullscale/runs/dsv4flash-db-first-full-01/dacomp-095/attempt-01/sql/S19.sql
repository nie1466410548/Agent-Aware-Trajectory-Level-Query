SELECT 
  paid_retention_rate_month,
  COUNT(*) as n,
  AVG(active_months) as avg_am,
  AVG(days_span) as avg_ds,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY paid_retention_rate_month
ORDER BY paid_retention_rate_month