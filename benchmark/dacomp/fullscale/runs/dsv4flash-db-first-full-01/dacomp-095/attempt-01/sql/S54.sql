SELECT 
  strftime('%Y-%m-%d', scheduled_to_send_at) as send_date,
  CAMPAIGN_TYPE,
  campaign_name
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
ORDER BY send_date
LIMIT 30