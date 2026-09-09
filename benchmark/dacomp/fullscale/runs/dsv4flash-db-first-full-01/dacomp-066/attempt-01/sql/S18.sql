SELECT job_id, name, hiring_managers, recruiters, sourcers,
       count_total_interviews, count_completed_interviews,
       count_total_applications, count_completed_interviews
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
LIMIT 10