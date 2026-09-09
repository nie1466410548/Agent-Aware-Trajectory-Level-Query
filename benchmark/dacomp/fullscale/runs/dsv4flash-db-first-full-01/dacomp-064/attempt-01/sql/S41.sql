-- Project category distribution for target stakeholders' issues
SELECT 
  p.project_category_id,
  COUNT(*) AS n_issues,
  COUNT(DISTINCT i.assignee_user_id) AS n_stakeholders,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY p.project_category_id
ORDER BY n_issues DESC