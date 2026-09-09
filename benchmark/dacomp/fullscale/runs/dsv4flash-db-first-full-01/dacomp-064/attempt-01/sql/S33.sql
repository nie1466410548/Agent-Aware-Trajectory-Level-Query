-- Check if daily assignee IDs match stakeholder IDs
SELECT COUNT(DISTINCT d.assignee) AS daily_assignee_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN d.assignee END) AS matched_to_stakeholders
FROM (SELECT DISTINCT assignee FROM jira__daily_issue_field_history) d
LEFT JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id