SELECT 
  flow_name,
  trigger_type,
  email_open_rate,
  email_click_to_open_rate,
  total_count_unique_people,
  count_placed_order,
  gmv_net
FROM klaviyo__flows
WHERE status = 'LIVE'
ORDER BY gmv_net DESC
LIMIT 15