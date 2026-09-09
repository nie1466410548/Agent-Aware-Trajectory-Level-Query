-- Primary risk drivers among false prosperity projects
SELECT primary_risk_driver, COUNT(*) as cnt
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
GROUP BY primary_risk_driver
ORDER BY cnt DESC