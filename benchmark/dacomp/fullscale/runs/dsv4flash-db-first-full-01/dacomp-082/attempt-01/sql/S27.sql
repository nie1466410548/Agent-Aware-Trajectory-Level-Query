WITH sms_users AS (
  SELECT * FROM qualtrics__contact WHERE count_surveys_sent_sms > 0
)
SELECT 
  NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_ltv,
  AVG(total_count_completed_surveys) AS avg_ltv,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS sms_comp_rate
FROM sms_users
GROUP BY quartile
ORDER BY quartile