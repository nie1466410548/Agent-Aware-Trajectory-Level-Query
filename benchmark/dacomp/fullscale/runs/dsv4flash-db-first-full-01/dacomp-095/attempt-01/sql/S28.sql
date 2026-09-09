SELECT 
  trigger_type,
  COUNT(*) as n_flows,
  AVG(email_open_rate) as avg_open_rate,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(total_count_unique_people) as avg_audience,
  AVG(count_placed_order) as avg_orders,
  AVG(gmv_net) as avg_gmv_net
FROM klaviyo__flows
GROUP BY trigger_type
ORDER BY avg_gmv_net DESC