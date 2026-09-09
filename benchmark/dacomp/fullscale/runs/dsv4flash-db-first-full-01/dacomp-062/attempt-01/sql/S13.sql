SELECT 
  trajectory_status,
  COUNT(*) AS n,
  AVG(complexity_risk_score) AS avg_complexity,
  AVG(success_probability) AS avg_success,
  AVG(delivered_value_points) AS avg_delivered,
  AVG(value_delivery_percentage) AS avg_vdp
FROM jira__project_risk_assessment
GROUP BY trajectory_status
ORDER BY avg_success ASC