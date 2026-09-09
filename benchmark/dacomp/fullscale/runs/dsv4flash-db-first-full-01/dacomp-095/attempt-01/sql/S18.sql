SELECT 
  has_30day_retention,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders
FROM klaviyo__persons
GROUP BY has_30day_retention