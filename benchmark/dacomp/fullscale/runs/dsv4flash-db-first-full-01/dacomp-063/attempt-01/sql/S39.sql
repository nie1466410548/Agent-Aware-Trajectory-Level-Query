SELECT primary_risk_factor, COUNT(*) as cnt, AVG(overall_health_score) as avg_health
FROM jira__project_risk_assessment
GROUP BY primary_risk_factor
ORDER BY cnt DESC