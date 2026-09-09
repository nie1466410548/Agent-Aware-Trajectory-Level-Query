
  SELECT person_id, timezone, 
         count_received_email, count_opened_email, count_clicked_email,
         email_open_rate, 
         active_retention_rate_week, active_retention_rate_month,
         active_days, active_weeks, active_months,
         days_span, weeks_span, months_span,
         has_7day_retention, has_30day_retention,
         count_placed_order, count_ordered_product,
         sum_revenue_placed_order, sum_revenue_ordered_product,
         first_event_on, last_event_on
  FROM klaviyo__persons
