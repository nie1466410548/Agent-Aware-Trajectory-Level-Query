SELECT 
  project_category,
  project_type,
  SUM(count_email_survey_responses) AS email_resp,
  SUM(count_email_completed_survey_responses) AS email_comp,
  SUM(count_sms_survey_responses) AS sms_resp,
  SUM(count_sms_completed_survey_responses) AS sms_comp,
  SUM(count_social_media_survey_responses) AS social_resp,
  SUM(count_social_media_completed_survey_responses) AS social_comp,
  SUM(count_uncategorized_survey_responses) AS web_mobile_resp,
  SUM(count_uncategorized_completed_survey_responses) AS web_mobile_comp
FROM qualtrics__survey
GROUP BY project_category, project_type
ORDER BY project_category, project_type