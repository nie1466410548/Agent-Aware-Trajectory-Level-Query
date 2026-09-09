SELECT COUNT(*) AS total, COUNT(DISTINCT interview_id) AS distinct_interviews,
       COUNT(DISTINCT application_id || '_' || interview_id) AS distinct_app_interview
FROM greenhouse__interview_enhanced