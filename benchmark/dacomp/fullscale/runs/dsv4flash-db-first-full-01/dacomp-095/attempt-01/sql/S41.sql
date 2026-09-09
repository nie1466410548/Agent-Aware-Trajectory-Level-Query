SELECT 
  strftime('%Y-%m', scheduled_to_send_at) as month,
  COUNT(*) as n_campaigns,
  AVG(email_open_rate) as avg_open,
  AVG(gmv_net) as avg_gmv
FROM klaviyo__campaigns
GROUP BY month
ORDER BY month