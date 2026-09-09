SELECT 
  CASE 
    WHEN active_months <= 2 THEN 'Cold Start'
    WHEN active_months = 3 THEN 'Growth'
    WHEN active_months = 4 THEN 'Mature'
    ELSE 'Peak'
  END as lifecycle_stage,
  COUNT(*) as n_persons,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_active_months,
  AVG(paid_retained_month_count) as avg_paid_retained_months,
  AVG(paid_retention_rate_month) as avg_paid_retention_rate,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open_rate,
  AVG(count_received_email) as avg_emails_received,
  AVG(count_clicked_email) as avg_clicks,
  AVG(active_retention_rate_month) as avg_active_ret_rate
FROM klaviyo__persons
GROUP BY lifecycle_stage
ORDER BY avg_active_months