SELECT 
  'email' AS channel,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed,
  SUM(total_count_completed_surveys) AS total_lifecycle_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS email_complete_rate,
  SUM(count_surveys_completed_email) AS total_email_completed,
  SUM(count_surveys_completed_sms) AS total_sms_completed
FROM qualtrics__contact
WHERE count_surveys_sent_email > 0
UNION ALL
SELECT 'sms',
  COUNT(*),
  AVG(total_count_completed_surveys),
  SUM(total_count_completed_surveys),
  AVG(avg_survey_progress_pct),
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)),
  SUM(count_surveys_completed_email),
  SUM(count_surveys_completed_sms)
FROM qualtrics__contact
WHERE count_surveys_sent_sms > 0