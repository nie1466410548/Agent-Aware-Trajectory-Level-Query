SELECT 
  risk_category,
  COUNT(*) AS n,
  AVG(complexity_risk_score) AS avg_complexity,
  AVG(success_probability) AS avg_success,
  AVG(total_risk_score) AS avg_total_risk,
  AVG(overall_health_score) AS avg_health
FROM jira__project_risk_assessment
GROUP BY risk_category
ORDER BY avg_success ASC