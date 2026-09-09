SELECT ae.sourced_from,
       ROUND(AVG(cs.candidate_quality_score), 2) as avg_quality,
       ROUND(AVG(cs.avg_interview_score), 2) as avg_interview_score,
       ROUND(AVG(cs.interview_success_rate), 2) as avg_int_success
FROM greenhouse__application_enhanced ae
JOIN greenhouse__candidate_summary cs USING (candidate_id)
GROUP BY ae.sourced_from