
SELECT ie.overall_recommendation, ie.duration_interview_minutes,
       ie.interview_name, ie.job_parent_departments,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.duration_interview_minutes IS NOT NULL
