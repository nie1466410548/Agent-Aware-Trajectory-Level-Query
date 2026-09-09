
SELECT scd.scorecard_id, scd.rating, scd.attribute_name,
       scd.overall_recommendation, scd.interview_name, scd.application_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.overall_recommendation IS NOT NULL
