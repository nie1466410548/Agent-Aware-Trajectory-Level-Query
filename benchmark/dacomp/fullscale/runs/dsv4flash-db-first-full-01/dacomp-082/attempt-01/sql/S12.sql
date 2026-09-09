SELECT 
  COUNT(*) AS total_contacts,
  SUM(CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END) AS email_contacts,
  SUM(CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS sms_contacts,
  SUM(CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS multi_channel_contacts,
  SUM(count_surveys_sent_email) AS total_email_sent,
  SUM(count_surveys_sent_sms) AS total_sms_sent,
  SUM(count_surveys_opened_email) AS total_email_opened,
  SUM(count_surveys_opened_sms) AS total_sms_opened,
  SUM(count_surveys_started_email) AS total_email_started,
  SUM(count_surveys_started_sms) AS total_sms_started,
  SUM(count_surveys_completed_email) AS total_email_completed,
  SUM(count_surveys_completed_sms) AS total_sms_completed
FROM qualtrics__contact