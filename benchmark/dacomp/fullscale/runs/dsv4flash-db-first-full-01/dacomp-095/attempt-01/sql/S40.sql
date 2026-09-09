SELECT 
  campaign_variation_key,
  COUNT(*) as n,
  AVG(email_open_rate) as avg_open,
  AVG(gmv_net) as avg_gmv
FROM klaviyo__campaigns
GROUP BY campaign_variation_key