SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-10-02' AND '2024-12-31'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type