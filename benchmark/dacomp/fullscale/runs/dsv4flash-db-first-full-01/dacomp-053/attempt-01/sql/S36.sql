SELECT 
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(quality_percentage),1) avg_quality,
  ROUND(AVG(risk_percentage),1) avg_risk,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab
FROM asana__project_analytics
WHERE health_grade = 'A'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'B'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'C'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'D'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'F'