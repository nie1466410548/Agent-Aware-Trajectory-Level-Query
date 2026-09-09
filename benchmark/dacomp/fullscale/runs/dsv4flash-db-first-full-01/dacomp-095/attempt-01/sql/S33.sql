SELECT 
  CAMPAIGN_TYPE,
  MIN(scheduled_to_send_at) as first_sent,
  MAX(scheduled_to_send_at) as last_sent,
  AVG(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END) as conversion_rate
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY first_sent