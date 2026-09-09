SELECT risk_category, COUNT(*) as cnt, AVG(overall_health_score) as avg_health, AVG(total_risk_score) as avg_risk, AVG(complexity_risk_score) as avg_complexity
FROM jira__project_risk_assessment
GROUP BY risk_category