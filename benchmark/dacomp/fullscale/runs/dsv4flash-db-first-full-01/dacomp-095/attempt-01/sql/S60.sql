-- Emails per month distribution to inform frequency recommendations
SELECT 
  CASE 
    WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo'
    WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo'
    WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo'
    ELSE '40+ emails/mo'
  END as intensity,
  COUNT(*) as n,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY intensity
ORDER BY intensity