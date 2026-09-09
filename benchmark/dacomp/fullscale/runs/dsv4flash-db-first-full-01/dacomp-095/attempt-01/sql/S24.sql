SELECT 
  CASE 
    WHEN count_clicked_email = 0 THEN 'no_clicks'
    WHEN count_clicked_email <= 5 THEN 'few_clicks'
    WHEN count_clicked_email <= 10 THEN 'some_clicks'
    ELSE 'many_clicks'
  END as click_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(count_placed_order) as avg_orders,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY click_segment
ORDER BY avg_orders DESC