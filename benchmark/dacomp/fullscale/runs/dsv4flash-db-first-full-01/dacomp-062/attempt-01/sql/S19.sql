SELECT 
  primary_risk_driver,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(overall_health_score),2) AS avg_health
FROM jira__project_risk_assessment
GROUP BY primary_risk_driver
ORDER BY avg_success ASC