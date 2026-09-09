SELECT account_id, date_day, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n_camps, COUNT(DISTINCT campaign_id) AS n_ids
FROM google_ads__campaign_report
GROUP BY account_id, date_day, advertising_channel_type, advertising_channel_subtype
HAVING n_camps > 1
LIMIT 10