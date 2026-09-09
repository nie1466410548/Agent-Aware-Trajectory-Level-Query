SELECT 
  'email' AS channel, project_category,
  SUM(count_email_completed_survey_responses) * 1.0 / NULLIF(SUM(count_email_survey_responses),0) AS completion_rate
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'sms', project_category,
  SUM(count_sms_completed_survey_responses) * 1.0 / NULLIF(SUM(count_sms_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'social', project_category,
  SUM(count_social_media_completed_survey_responses) * 1.0 / NULLIF(SUM(count_social_media_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'web_mobile', project_category,
  SUM(count_uncategorized_completed_survey_responses) * 1.0 / NULLIF(SUM(count_uncategorized_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
ORDER BY channel, project_category