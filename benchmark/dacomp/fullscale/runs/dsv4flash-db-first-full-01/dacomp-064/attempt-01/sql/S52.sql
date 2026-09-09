
SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE NOT (s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3)
  AND i.resolved_at IS NOT NULL
