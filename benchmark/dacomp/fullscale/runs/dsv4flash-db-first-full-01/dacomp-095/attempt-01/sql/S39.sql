SELECT 
  has_converted,
  AVG(email_open_rate_touch) as avg_open_touch,
  AVG(email_click_to_open_rate_touch) as avg_ctr_touch,
  AVG(touch_span_days) as avg_touch_span,
  AVG(count_received_email) as avg_emails,
  AVG(net_revenue_touch) as avg_net_rev
FROM klaviyo__person_campaign_flow
GROUP BY has_converted