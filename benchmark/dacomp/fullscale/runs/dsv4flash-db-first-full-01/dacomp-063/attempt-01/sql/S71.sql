-- Engagement risk status by performance tier
SELECT t.performance_tier, s.engagement_risk_status, COUNT(*) as cnt
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY t.performance_tier, s.engagement_risk_status
ORDER BY t.performance_tier, s.engagement_risk_status