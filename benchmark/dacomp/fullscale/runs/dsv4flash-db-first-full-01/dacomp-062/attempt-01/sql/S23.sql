SELECT success_probability, COUNT(*) AS n
FROM jira__project_risk_assessment
GROUP BY success_probability
ORDER BY success_probability