SELECT 
  CAMPAIGN_TYPE,
  COUNT(*) as n_campaigns,
  AVG(email_open_rate) as avg_open_rate,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(total_count_unique_people) as avg_audience,
  AVG(count_placed_order) as avg_orders,
  AVG(gmv_net) as avg_gmv_net,
  AVG(count_clicked_email) as avg_clicks,
  AVG(count_received_email) as avg_received
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY avg_gmv_net DESC