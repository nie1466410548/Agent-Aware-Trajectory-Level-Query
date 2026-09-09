SELECT engagement_risk_status, COUNT(*) as cnt
FROM jira__stakeholder_engagement_insights
GROUP BY engagement_risk_status