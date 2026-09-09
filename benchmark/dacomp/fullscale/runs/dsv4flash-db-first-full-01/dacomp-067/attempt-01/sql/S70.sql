
SELECT scd.attribute_name, scd.rating, scd.overall_recommendation,
       scd.interview_name, scd.job_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
LIMIT 1000
