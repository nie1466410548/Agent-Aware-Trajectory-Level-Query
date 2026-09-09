SELECT trajectory_status, COUNT(*) as cnt, AVG(overall_health_score) as avg_health, AVG(health_risk_score) as avg_health_risk
FROM jira__project_risk_assessment
GROUP BY trajectory_status