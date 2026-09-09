-- Check if issue assignee_user_id matches stakeholder IDs
SELECT COUNT(DISTINCT i.assignee_user_id) AS issue_assignee_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN i.assignee_user_id END) AS matched_to_stakeholders
FROM (SELECT DISTINCT assignee_user_id FROM jira__issue_enhanced) i
LEFT JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id