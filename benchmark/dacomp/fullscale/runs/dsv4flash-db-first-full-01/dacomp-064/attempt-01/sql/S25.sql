-- Check if stakeholder_id matches user_id
SELECT s.stakeholder_id, u.user_id, s.user_display_name, u.user_display_name
FROM jira__stakeholder_engagement_insights s
LEFT JOIN jira__user_enhanced u ON s.stakeholder_id = u.user_id
LIMIT 10