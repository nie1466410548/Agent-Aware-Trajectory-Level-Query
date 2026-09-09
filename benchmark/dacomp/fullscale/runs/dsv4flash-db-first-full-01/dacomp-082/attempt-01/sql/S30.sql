SELECT 
  project_category,
  SUM(count_email_survey_responses) AS email_r,
  SUM(count_sms_survey_responses) AS sms_r,
  SUM(count_social_media_survey_responses) AS social_r,
  SUM(count_uncategorized_survey_responses) AS uncat_r,
  SUM(count_personal_link_survey_responses) AS plink_r,
  SUM(count_qr_code_survey_responses) AS qr_r
FROM qualtrics__survey
GROUP BY project_category
ORDER BY project_category