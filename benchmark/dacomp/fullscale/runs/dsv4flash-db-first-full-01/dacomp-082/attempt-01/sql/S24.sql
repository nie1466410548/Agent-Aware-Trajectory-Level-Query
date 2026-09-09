SELECT 
  CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END AS email_user,
  CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END AS sms_user,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  AVG(count_surveys_sent_email) AS avg_email_sent,
  AVG(count_surveys_sent_sms) AS avg_sms_sent,
  AVG(count_surveys_opened_email * 1.0/NULLIF(count_surveys_sent_email,0)) AS email_open_rate,
  AVG(count_surveys_opened_sms * 1.0/NULLIF(count_surveys_sent_sms,0)) AS sms_open_rate,
  AVG(count_surveys_completed_email * 1.0/NULLIF(count_surveys_sent_email,0)) AS email_complete_rate,
  AVG(count_surveys_completed_sms * 1.0/NULLIF(count_surveys_sent_sms,0)) AS sms_complete_rate
FROM qualtrics__contact
GROUP BY email_user, sms_user
ORDER BY email_user, sms_user