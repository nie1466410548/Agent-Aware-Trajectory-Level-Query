SELECT 
  active_months,
  COUNT(*) as n,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds,
  AVG(active_retention_rate_month) as avg_arm
FROM klaviyo__persons
GROUP BY active_months
ORDER BY active_months