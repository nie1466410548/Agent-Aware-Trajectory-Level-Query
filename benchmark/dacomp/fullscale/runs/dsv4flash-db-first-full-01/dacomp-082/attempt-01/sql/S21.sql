SELECT 
  channel,
  SUM(comp) * 1.0 / SUM(resp) AS overall_completion,
  SUM(resp) AS total_resp,
  SUM(comp) AS total_comp
FROM (
  SELECT 'email' AS channel, project_category,
    SUM(count_email_survey_responses) AS resp, SUM(count_email_completed_survey_responses) AS comp
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'sms', project_category,
    SUM(count_sms_survey_responses), SUM(count_sms_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'social', project_category,
    SUM(count_social_media_survey_responses), SUM(count_social_media_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'web_mobile', project_category,
    SUM(count_uncategorized_survey_responses), SUM(count_uncategorized_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
)
GROUP BY channel
ORDER BY channel