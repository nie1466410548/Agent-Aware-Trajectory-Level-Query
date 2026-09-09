-- Monthly resolution trend for target stakeholders
SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  COUNT(*) AS n_resolved,
  ROUND(AVG((julianday(i.resolved_at) - julianday(i.created_at))*1.0),2) AS avg_close_days
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL
GROUP BY strftime('%Y-%m', i.resolved_at)
ORDER BY month