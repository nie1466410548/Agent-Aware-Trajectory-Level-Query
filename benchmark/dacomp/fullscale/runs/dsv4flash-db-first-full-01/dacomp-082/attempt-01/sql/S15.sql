SELECT 
  CASE 
    WHEN total_count_completed_surveys = 0 THEN '0_inactive'
    WHEN total_count_completed_surveys <= 2 THEN '1_low'
    WHEN total_count_completed_surveys <= 6 THEN '2_mid'
    ELSE '3_high'
  END AS cohort,
  COUNT(*) AS users,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  AVG(total_count_surveys) AS avg_surveys_sent,
  AVG(count_surveys_completed_email) AS avg_email_completed,
  AVG(count_surveys_completed_sms) AS avg_sms_completed,
  AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_open_rate,
  AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_open_rate
FROM qualtrics__contact
GROUP BY cohort
ORDER BY cohort