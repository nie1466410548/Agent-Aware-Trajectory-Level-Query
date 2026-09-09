SELECT 
  quartile,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_completed,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  SUM(count_surveys_completed_email) AS email_completed,
  SUM(count_surveys_completed_sms) AS sms_completed
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile
  FROM qualtrics__contact
)
GROUP BY quartile
ORDER BY quartile