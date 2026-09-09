SELECT project_category,
  COUNT(*) AS total_surveys,
  SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_email,
  SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_sms,
  SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_social,
  SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_uncat
FROM qualtrics__survey
GROUP BY project_category