SELECT 
  CAMPAIGN_TYPE,
  AVG(count_placed_order / NULLIF(count_received_email, 0)) as orders_per_received,
  AVG(count_opened_email / NULLIF(count_received_email, 0)) as open_per_received,
  AVG(count_clicked_email / NULLIF(count_received_email, 0)) as click_per_received,
  AVG(gmv_net / NULLIF(count_received_email, 0)) as gmv_per_received,
  AVG(gmv_net / NULLIF(count_placed_order, 0)) as aov
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_received DESC