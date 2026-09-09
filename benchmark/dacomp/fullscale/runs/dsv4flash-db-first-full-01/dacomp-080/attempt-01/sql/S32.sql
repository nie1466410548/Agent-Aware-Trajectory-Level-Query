SELECT 
  CASE WHEN total_count_surveys=1 THEN 'one' 
       WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5'
       WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10'
       WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20'
       WHEN total_count_surveys > 20 THEN '21+' END AS bucket,
  COUNT(*) AS n
FROM qualtrics__contact
GROUP BY bucket ORDER BY bucket