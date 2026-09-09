SELECT 
  CASE 
    WHEN email_open_rate >= 0.5 THEN 'high_open'
    WHEN email_open_rate >= 0.3 THEN 'medium_open'
    ELSE 'low_open'
  END as open_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(days_span) as avg_ds,
  AVG(count_placed_order) as avg_orders,
  AVG(has_converted) as avg_converted
FROM klaviyo__persons
GROUP BY open_segment
ORDER BY avg_prr DESC