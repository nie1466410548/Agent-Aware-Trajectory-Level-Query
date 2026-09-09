SELECT 
  CASE 
    WHEN count_placed_order = 0 THEN 'No Orders'
    WHEN count_placed_order = 1 THEN '1 Order'
    WHEN count_placed_order <= 3 THEN '2-3 Orders'
    ELSE '4+ Orders'
  END as order_tier,
  COUNT(*) as n,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_am,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY order_tier
ORDER BY avg_orders DESC