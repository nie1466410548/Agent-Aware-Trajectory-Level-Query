SELECT 
  active_months,
  AVG(count_placed_order) as avg_orders,
  AVG(count_received_email) as avg_emails,
  AVG(count_opened_email) as avg_opens,
  AVG(count_clicked_email) as avg_clicks,
  AVG(email_open_rate) as avg_open_rate,
  AVG(days_span) as avg_days_span,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY active_months
ORDER BY active_months