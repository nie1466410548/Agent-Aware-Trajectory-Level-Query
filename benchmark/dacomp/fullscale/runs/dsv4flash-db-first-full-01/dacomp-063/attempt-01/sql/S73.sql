-- Count of projects with health > 75 and "Monitor Hidden Risks" recommendation
SELECT COUNT(*) FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND strategic_priority_recommendation = 'High Priority - Monitor Hidden Risks'