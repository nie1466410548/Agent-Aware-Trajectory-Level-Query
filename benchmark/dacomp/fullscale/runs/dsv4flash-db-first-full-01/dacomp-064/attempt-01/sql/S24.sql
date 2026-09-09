-- Check if stakeholder user_display_names match assignee_name
SELECT s.user_display_name, s.stakeholder_id, i.assignee_name, i.assignee_user_id
FROM jira__stakeholder_engagement_insights s
JOIN jira__issue_enhanced i ON s.user_display_name = i.assignee_name
LIMIT 10