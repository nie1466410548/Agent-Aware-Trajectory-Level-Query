SELECT 
  SUM(CASE WHEN is_finished_with_survey=1 AND survey_response_status=1 THEN 1 ELSE 0 END) AS both_1,
  SUM(CASE WHEN is_finished_with_survey=0 AND survey_response_status=0 THEN 1 ELSE 0 END) AS both_0,
  SUM(CASE WHEN is_finished_with_survey=0 AND survey_response_status=1 THEN 1 ELSE 0 END) AS f0_s1,
  SUM(CASE WHEN is_finished_with_survey=1 AND survey_response_status=0 THEN 1 ELSE 0 END) AS f1_s0
FROM qualtrics__response