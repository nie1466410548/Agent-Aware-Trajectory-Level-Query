SELECT campaign_name, campaign_subject_line, COUNT(*) AS n_events_by_campaign
FROM klaviyo__events 
GROUP BY campaign_name, campaign_subject_line