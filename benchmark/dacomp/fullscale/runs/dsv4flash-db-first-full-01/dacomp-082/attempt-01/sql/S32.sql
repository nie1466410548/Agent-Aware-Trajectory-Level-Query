SELECT project_category,
  SUM(count_email_survey_responses) AS email_r, SUM(count_email_completed_survey_responses) AS email_c,
  SUM(count_sms_survey_responses) AS sms_r, SUM(count_sms_completed_survey_responses) AS sms_c,
  SUM(count_social_media_survey_responses) AS social_r, SUM(count_social_media_completed_survey_responses) AS social_c,
  SUM(count_uncategorized_survey_responses) AS wm_r, SUM(count_uncategorized_completed_survey_responses) AS wm_c
FROM qualtrics__survey
GROUP BY project_category