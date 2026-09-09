WITH camp AS (
  SELECT campaign_id, account_id, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) > 120
)
SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype,
       c.last_date AS camp_last_date,
       MAX(substr(a.date_day,1,10)) AS acq_last_date,
       MIN(substr(a.date_day,1,10)) AS acq_first_date,
       COUNT(a.rowid) AS n_rows
FROM camp c
JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
GROUP BY c.campaign_id
ORDER BY c.campaign_id