SELECT 
  COUNT(*) AS n,
  SUM(CASE WHEN total_count_completed_surveys=0 THEN 1 ELSE 0 END) AS zero_completed,
  AVG(total_count_surveys) AS avg_sent,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(1.0*total_count_completed_surveys/NULLIF(total_count_surveys,0)) AS avg_completion_rate,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_email) AS avg_comp_email,
  AVG(count_surveys_completed_sms) AS avg_comp_sms
FROM qualtrics__contact