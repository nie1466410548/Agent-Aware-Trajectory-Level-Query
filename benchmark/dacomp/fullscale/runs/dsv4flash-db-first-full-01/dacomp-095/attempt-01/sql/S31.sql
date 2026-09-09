WITH speed_tiers AS (
  SELECT *,
    active_days * 1.0 / days_span as activity_density,
    months_span - active_months as gap_months,
    CASE 
      WHEN active_days * 1.0 / days_span >= 0.95 THEN 'Very High Density'
      WHEN active_days * 1.0 / days_span >= 0.85 THEN 'High Density'
      WHEN active_days * 1.0 / days_span >= 0.75 THEN 'Medium Density'
      ELSE 'Low Density'
    END as density_segment
  FROM klaviyo__persons
)
SELECT 
  density_segment,
  COUNT(*) as n,
  AVG(activity_density) as avg_density,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_active_months
FROM speed_tiers
GROUP BY density_segment
ORDER BY avg_density DESC