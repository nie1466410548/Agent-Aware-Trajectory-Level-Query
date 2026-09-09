-- Touchpoint path: typical sequence of campaign types
WITH sent AS (
  SELECT CAMPAIGN_TYPE, scheduled_to_send_at,
         ROW_NUMBER() OVER (ORDER BY scheduled_to_send_at) as seq
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
)
SELECT seq, scheduled_to_send_at, CAMPAIGN_TYPE
FROM sent
ORDER BY seq
LIMIT 40