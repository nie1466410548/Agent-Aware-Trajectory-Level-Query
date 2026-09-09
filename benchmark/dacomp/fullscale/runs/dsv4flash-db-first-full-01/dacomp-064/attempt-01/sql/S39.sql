-- Project type distribution for target stakeholders
SELECT i.project_name, i.issue_type, COUNT(*) AS n_issues,
       ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
       ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY i.project_name, i.issue_type
ORDER BY n_issues DESC
LIMIT 30