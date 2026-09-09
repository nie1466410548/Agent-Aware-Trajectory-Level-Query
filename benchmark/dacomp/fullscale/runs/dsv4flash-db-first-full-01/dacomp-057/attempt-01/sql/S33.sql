SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       MIN(date_day) AS first_date, MAX(date_day) AS last_date,
       CAST(julianday(MAX(date_day)) - julianday(MIN(date_day)) AS INTEGER) AS days_running
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY days_running DESC
LIMIT 20