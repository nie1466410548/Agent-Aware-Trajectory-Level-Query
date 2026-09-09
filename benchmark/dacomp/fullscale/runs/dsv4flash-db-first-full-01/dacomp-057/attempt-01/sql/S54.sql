WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
)
SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype, c.days_running,
       COUNT(a.rowid) AS matched_rows
FROM camp c
LEFT JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
GROUP BY c.campaign_id
HAVING matched_rows = 0
ORDER BY c.campaign_id