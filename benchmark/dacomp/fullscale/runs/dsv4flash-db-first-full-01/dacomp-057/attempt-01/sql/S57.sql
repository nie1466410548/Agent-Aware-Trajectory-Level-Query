SELECT account_id, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n, MIN(substr(date_day,1,10)) AS min_d, MAX(substr(date_day,1,10)) AS max_d
FROM google_ads__customer_acquisition_analysis
WHERE account_id IN ('ACC_HLTH_001','ACC_FIN_001','ACC_GAME_001','ACC_SAAS_001')
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype
ORDER BY account_id, advertising_channel_type