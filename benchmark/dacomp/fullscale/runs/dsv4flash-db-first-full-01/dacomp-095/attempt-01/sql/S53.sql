SELECT 
  CAMPAIGN_TYPE,
  AVG(product_view_to_order_rate_campaign) as avg_pv_to_order,
  AVG(count_ordered_product / NULLIF(count_placed_order,0)) as items_per_order,
  AVG(gmv_net / NULLIF(total_count_unique_people,0)) as gmv_per_person
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_person DESC