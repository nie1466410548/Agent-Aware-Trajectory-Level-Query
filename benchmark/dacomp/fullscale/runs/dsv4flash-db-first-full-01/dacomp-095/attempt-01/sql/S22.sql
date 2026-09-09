SELECT 
  months_span - active_months as inactive_months,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds
FROM klaviyo__persons
GROUP BY inactive_months
ORDER BY inactive_months