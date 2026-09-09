SELECT 
  CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END as health_band,
  risk_category,
  COUNT(*) as cnt,
  AVG(overall_health_score) as avg_health,
  AVG(total_risk_score) as avg_total_risk,
  AVG(complexity_risk_score) as avg_complexity,
  AVG(success_probability) as avg_success
FROM jira__project_risk_assessment
GROUP BY health_band, risk_category
ORDER BY health_band, cnt DESC