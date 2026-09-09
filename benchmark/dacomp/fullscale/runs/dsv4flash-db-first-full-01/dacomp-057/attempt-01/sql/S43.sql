SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2025-05-22' AND '2025-06-21'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type