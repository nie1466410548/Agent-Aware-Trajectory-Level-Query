SELECT DISTINCT c.advertising_channel_type, c.advertising_channel_subtype, c.campaign_name, c.campaign_id, c.status
FROM google_ads__campaign_report c
ORDER BY c.campaign_name