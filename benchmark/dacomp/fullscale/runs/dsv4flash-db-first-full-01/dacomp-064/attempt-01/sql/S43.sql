-- Per-target-stakeholder issue-level performance metrics
SELECT 
  s.stakeholder_id,
  COUNT(i.issue_id) AS n_issues_handled,
  SUM(CASE WHEN i.resolved_at IS NOT NULL THEN 1 ELSE 0 END) AS n_resolved,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio,
  ROUND(SUM(i.time_spent_seconds)/3600.0,1) AS total_hours_spent,
  ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
  COUNT(DISTINCT i.project_id) AS n_projects_worked,
  COUNT(DISTINCT i.issue_type) AS n_issue_types
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY s.stakeholder_id