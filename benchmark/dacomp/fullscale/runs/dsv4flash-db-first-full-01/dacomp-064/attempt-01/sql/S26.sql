-- How many distinct names in issues match stakeholder names
SELECT COUNT(DISTINCT s.stakeholder_id) AS stakeholders_with_issues_as_assignee
FROM jira__stakeholder_engagement_insights s
JOIN jira__issue_enhanced i ON s.user_display_name = i.assignee_name