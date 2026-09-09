SELECT 
  CASE 
    WHEN days_span <= 60 THEN 'Fast (≤60d)'
    WHEN days_span <= 90 THEN 'Medium (61-90d)'
    WHEN days_span <= 120 THEN 'Slow (91-120d)'
    ELSE 'Very Slow (>120d)'
  END as speed_group,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(active_days * 1.0 / days_span) as avg_density
FROM klaviyo__persons
GROUP BY speed_group
ORDER BY speed_group