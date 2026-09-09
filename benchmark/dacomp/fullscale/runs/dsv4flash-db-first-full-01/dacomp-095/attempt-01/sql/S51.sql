
SELECT person_id, days_span, active_days, active_months, months_span,
       paid_retained_month_count, paid_retention_rate_month,
       active_retention_rate_month, email_open_rate, count_received_email,
       count_opened_email, count_clicked_email, count_placed_order,
       sum_revenue_placed_order, count_viewed_product, has_7day_retention, has_30day_retention
FROM klaviyo__persons
