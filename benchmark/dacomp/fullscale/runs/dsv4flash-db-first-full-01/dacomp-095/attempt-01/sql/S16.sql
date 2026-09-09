SELECT 
  CASE WHEN julianday(first_event_on) - julianday(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END as first_touch_seg,
  COUNT(*) as n,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY first_touch_seg