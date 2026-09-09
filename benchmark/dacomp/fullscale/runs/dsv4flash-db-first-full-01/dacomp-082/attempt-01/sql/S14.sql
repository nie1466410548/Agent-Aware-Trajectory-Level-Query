SELECT 
  SUM(count_survey_responses) AS total_responses,
  SUM(count_completed_survey_responses) AS total_completed,
  COUNT(*) AS n_surveys
FROM qualtrics__survey