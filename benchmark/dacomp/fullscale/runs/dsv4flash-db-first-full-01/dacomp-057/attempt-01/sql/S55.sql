SELECT account_id, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype
ORDER BY account_id, advertising_channel_type