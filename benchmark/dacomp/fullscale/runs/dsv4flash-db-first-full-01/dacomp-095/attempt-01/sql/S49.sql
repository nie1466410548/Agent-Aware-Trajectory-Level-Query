SELECT 
  CAMPAIGN_TYPE,
  AVG(email_open_rate) as avg_open,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(gmv_net / NULLIF(count_placed_order,0)) as aov,
  AVG(count_clicked_email / NULLIF(count_received_email,0)) as click_rate_received,
  AVG(count_placed_order / NULLIF(count_received_email,0)) as orders_per_recv,
  AVG(gmv_net / NULLIF(count_received_email,0)) as gmv_per_recv
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_recv DESC