SELECT 
  trajectory_status,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk,
  ROUND(AVG(health_risk_score),2) AS avg_health_risk,
  ROUND(AVG(schedule_risk_score),2) AS avg_schedule_risk,
  ROUND(AVG(resource_risk_score),2) AS avg_resource_risk,
  ROUND(AVG(scope_risk_score),2) AS avg_scope_risk
FROM jira__project_risk_assessment
GROUP BY trajectory_status
ORDER BY avg_total_risk DESC