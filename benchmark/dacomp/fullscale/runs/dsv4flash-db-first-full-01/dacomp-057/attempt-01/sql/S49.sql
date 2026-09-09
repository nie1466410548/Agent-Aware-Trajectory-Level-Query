SELECT substr(date_day,1,10) AS d, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-06-01' AND '2024-12-31'
GROUP BY d ORDER BY d