SELECT campaign_id, MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
       CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
FROM google_ads__campaign_report
WHERE campaign_id IN ('CMP_ACC_FIN_001_001','CMP_ACC_FIN_001_003','CMP_ACC_FIN_001_006','CMP_ACC_FIN_001_007')
GROUP BY campaign_id