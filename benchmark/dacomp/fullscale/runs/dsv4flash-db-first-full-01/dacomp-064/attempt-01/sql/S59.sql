
SELECT p.project_category_id, 
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  strftime('%Y-%m', i.resolved_at) AS month
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL AND i.resolved_at < '2025-11-01'
