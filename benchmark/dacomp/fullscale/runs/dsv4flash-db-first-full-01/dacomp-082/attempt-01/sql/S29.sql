SELECT quartile, COUNT(*) AS users, SUM(total_count_completed_surveys) AS total_ltv, 
       AVG(total_count_completed_surveys) AS avg_ltv,
       AVG(avg_survey_progress_pct) AS avg_progress
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile
  FROM qualtrics__contact
  WHERE count_surveys_sent_sms > 0
) sub
GROUP BY quartile
ORDER BY quartile