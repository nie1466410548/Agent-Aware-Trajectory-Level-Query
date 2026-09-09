SELECT status, COUNT(*) as cnt,
       AVG(candidate_quality_score) as avg_quality
FROM greenhouse__candidate_summary cs
JOIN greenhouse__application_enhanced ae USING (candidate_id)
GROUP BY status