SELECT 
  CASE 
    WHEN days_span <= 60 THEN 'fast_ramp'
    WHEN days_span <= 100 THEN 'medium_ramp' 
    WHEN days_span <= 140 THEN 'slow_ramp'
    ELSE 'very_slow_ramp'
  END as ramp_speed,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders
FROM klaviyo__persons
GROUP BY ramp_speed
ORDER BY ramp_speed