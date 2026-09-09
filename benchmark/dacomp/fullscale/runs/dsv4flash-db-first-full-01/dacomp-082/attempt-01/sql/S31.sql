SELECT 
  survey_status, COUNT(*) AS n,
  SUM(count_survey_responses) AS resp
FROM qualtrics__survey GROUP BY survey_status