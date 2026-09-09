SELECT 
  COUNT(*) AS users,
  AVG(count_surveys_sent_email) AS avg_email_sent,
  AVG(count_surveys_sent_sms) AS avg_sms_sent,
  AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_open,
  AVG(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_start,
  AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_complete,
  AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_open,
  AVG(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_start,
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_complete,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed
FROM qualtrics__contact