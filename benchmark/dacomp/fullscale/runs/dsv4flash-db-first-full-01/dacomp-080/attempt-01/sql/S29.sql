SELECT 
  n_survey_responses,
  COUNT(*) AS n_users,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM (
  SELECT recipient_email, COUNT(DISTINCT survey_response_id) AS n_survey_responses
  FROM qualtrics__response
  GROUP BY recipient_email
) t
GROUP BY n_survey_responses
ORDER BY n_survey_responses