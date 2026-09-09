SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
       CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running,
       CAST(julianday('2024-12-31') - julianday(MAX(substr(date_day,1,10))) AS INTEGER) AS days_since_last_data
FROM google_ads__campaign_report
GROUP BY campaign_id
HAVING days_running > 120
ORDER BY days_running DESC