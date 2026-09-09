SELECT campaign_id, variation_id, campaign_name, SUBJECT, SENT_AT,
       strftime('%Y-%m', SENT_AT) AS sent_month
FROM klaviyo__campaigns
ORDER BY SENT_AT
LIMIT 8