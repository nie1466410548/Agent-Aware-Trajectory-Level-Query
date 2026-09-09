
SELECT ie.application_id, ie.interviewer_name, ie.job_title,
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation,
       ie.interview_name,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
LEFT JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL
