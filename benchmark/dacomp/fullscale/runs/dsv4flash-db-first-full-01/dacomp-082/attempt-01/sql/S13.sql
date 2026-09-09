SELECT 
  SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_email,
  SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_sms,
  SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_social,
  SUM(CASE WHEN count_personal_link_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_plink,
  SUM(CASE WHEN count_qr_code_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_qr,
  SUM(CASE WHEN count_anonymous_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_anon,
  SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_uncat
FROM qualtrics__survey