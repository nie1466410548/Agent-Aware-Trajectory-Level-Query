-- Match daily reporter IDs to stakeholders
SELECT COUNT(DISTINCT d.reporter) AS daily_reporter_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN d.reporter END) AS matched
FROM (SELECT DISTINCT reporter FROM jira__daily_issue_field_history) d
LEFT JOIN jira__stakeholder_engagement_insights s ON d.reporter = s.stakeholder_id