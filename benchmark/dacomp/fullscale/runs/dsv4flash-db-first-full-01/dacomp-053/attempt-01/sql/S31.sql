SELECT 
  CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       ELSE 'Normal'
  END AS group_label,
  COUNT(*) AS n
FROM asana__project_analytics
GROUP BY group_label