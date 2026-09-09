SELECT pcf.person_id, pcf.last_touch_campaign_id, c.CAMPAIGN_TYPE, pcf.has_converted, pcf.email_open_rate_touch, pcf.email_click_to_open_rate_touch, pcf.net_revenue_touch
FROM klaviyo__person_campaign_flow pcf
LEFT JOIN klaviyo__campaigns c ON pcf.last_touch_campaign_id = c.campaign_id