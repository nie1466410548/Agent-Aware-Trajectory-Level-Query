WITH at_risk AS (
  SELECT *, 
    CASE WHEN paid_retention_rate_month < 1.0 THEN 'At_Risk_Winback' ELSE 'Retained' END as ret_segment
  FROM klaviyo__persons
)
SELECT 
  ret_segment,
  lifecycle_stage,
  COUNT(*) as n,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails
FROM (
  SELECT *,
    CASE 
      WHEN active_months <= 2 THEN 'Cold Start'
      WHEN active_months = 3 THEN 'Growth'
      WHEN active_months = 4 THEN 'Mature'
      ELSE 'Peak'
    END as lifecycle_stage,
    CASE WHEN paid_retention_rate_month < 1.0 THEN 'At_Risk_Winback' ELSE 'Retained' END as ret_segment
  FROM klaviyo__persons
) sub
GROUP BY ret_segment, lifecycle_stage
ORDER BY lifecycle_stage, ret_segment