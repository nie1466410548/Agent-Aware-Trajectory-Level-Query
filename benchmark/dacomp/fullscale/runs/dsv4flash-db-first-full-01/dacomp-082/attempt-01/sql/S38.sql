SELECT project_category, project_type,
  AVG(count_email_survey_responses) AS avg_email,
  AVG(count_sms_survey_responses) AS avg_sms,
  AVG(count_social_media_survey_responses) AS avg_social,
  AVG(count_uncategorized_survey_responses) AS avg_uncat,
  AVG(count_questions) AS avg_questions
FROM qualtrics__survey
GROUP BY project_category, project_type
ORDER BY project_category, project_type