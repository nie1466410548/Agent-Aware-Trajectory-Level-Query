SELECT COUNT(*) AS total_days, COUNT(DISTINCT account_id || '|' || substr(date_day,1,10)) AS acct_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-11-02' AND '2024-12-31'