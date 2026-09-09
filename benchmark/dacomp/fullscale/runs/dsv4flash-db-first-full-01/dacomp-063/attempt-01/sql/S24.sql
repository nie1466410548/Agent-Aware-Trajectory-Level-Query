SELECT recommended_intervention, COUNT(*) as cnt, AVG(overall_health_score) as avg_health
FROM jira__project_risk_assessment
GROUP BY recommended_intervention