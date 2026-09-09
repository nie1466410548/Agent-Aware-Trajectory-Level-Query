SELECT 
  CASE 
    WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both'
    WHEN count_surveys_sent_email > 0 THEN 'email_only'
    WHEN count_surveys_sent_sms > 0 THEN 'sms_only'
    ELSE 'neither'
  END AS channel_group,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_ltv,
  AVG(total_count_completed_surveys) AS avg_ltv,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  SUM(count_surveys_completed_email) AS email_completed,
  SUM(count_surveys_completed_sms) AS sms_completed
FROM qualtrics__contact
GROUP BY channel_group
ORDER BY channel_group