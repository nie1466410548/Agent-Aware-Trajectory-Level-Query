SELECT 
  CASE 
    WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant'
    WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant'
    ELSE 'balanced'
  END AS channel_pref,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration
FROM qualtrics__contact
GROUP BY channel_pref