
SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status
ORDER BY d.date_week
