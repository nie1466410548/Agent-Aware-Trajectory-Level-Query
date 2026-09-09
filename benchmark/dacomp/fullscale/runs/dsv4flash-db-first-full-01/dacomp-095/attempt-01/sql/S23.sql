SELECT 
  CASE 
    WHEN count_received_email <= 50 THEN 'low_freq'
    WHEN count_received_email <= 70 THEN 'med_freq'
    WHEN count_received_email <= 90 THEN 'high_freq'
    ELSE 'very_high_freq'
  END as freq_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(email_open_rate) as avg_open,
  AVG(count_unsubscribed) as avg_unsub
FROM klaviyo__persons
GROUP BY freq_segment
ORDER BY avg_orders DESC