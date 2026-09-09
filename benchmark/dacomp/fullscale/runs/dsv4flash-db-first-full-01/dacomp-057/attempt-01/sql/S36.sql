SELECT account_id, MIN(substr(date_day,1,10)) AS min_date, MAX(substr(date_day,1,10)) AS max_date, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id
ORDER BY account_id