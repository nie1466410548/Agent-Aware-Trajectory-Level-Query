-- Join team performance and stakeholder data on user ID
SELECT 
  t.overall_performance_score > 80 as high_performer,
  s.engagement_risk_status,
  COUNT(*) as cnt
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY high_performer, s.engagement_risk_status
ORDER BY high_performer, s.engagement_risk_status