SELECT
  CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END as paying,
  COUNT(*) as n,
  AVG(days_span) as avg_ds,
  AVG(active_months) as avg_am,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY paying