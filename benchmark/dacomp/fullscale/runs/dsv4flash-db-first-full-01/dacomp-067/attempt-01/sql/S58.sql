SELECT 
  CASE WHEN candidate_quality_score >= 4 THEN 'high_quality' ELSE 'low_quality' END as quality_tier,
  COUNT(*) as cnt,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
  AVG(candidate_quality_score) as avg_score
FROM greenhouse__application_enhanced ae
JOIN greenhouse__candidate_summary cs USING (candidate_id)
GROUP BY quality_tier