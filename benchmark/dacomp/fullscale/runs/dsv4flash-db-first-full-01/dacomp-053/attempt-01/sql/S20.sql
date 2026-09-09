SELECT 
  CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV'
       WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV'
       ELSE 'Other'
  END AS inversion_type,
  COUNT(*) AS n
FROM asana__project_analytics
GROUP BY inversion_type