SELECT project_category,
  COUNT(*) AS n,
  AVG(count_email_survey_responses) AS avg_email_resp,
  AVG(count_sms_survey_responses) AS avg_sms_resp,
  AVG(count_social_media_survey_responses) AS avg_social_resp,
  AVG(count_uncategorized_survey_responses) AS avg_uncat_resp,
  AVG(count_questions) AS avg_questions
FROM qualtrics__survey
GROUP BY project_category