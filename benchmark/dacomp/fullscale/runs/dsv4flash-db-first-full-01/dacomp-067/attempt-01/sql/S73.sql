
SELECT ie.application_id, ie.interviewer_name, ie.job_title, 
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation, ie.interviewer_is_hiring_manager,
       ae.status as app_status, ae.job_parent_departments as app_job_depts
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.job_parent_departments IS NOT NULL
