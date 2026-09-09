SELECT campaign_name, COUNT(*) AS n
FROM klaviyo__campaigns
GROUP BY campaign_name ORDER BY campaign_name