SELECT project_category, 
       COUNT(*) AS survey_count,
       SUM(count_survey_responses) AS total_responses,
       SUM(count_completed_survey_responses) AS total_completed
FROM qualtrics__survey 
GROUP BY project_category