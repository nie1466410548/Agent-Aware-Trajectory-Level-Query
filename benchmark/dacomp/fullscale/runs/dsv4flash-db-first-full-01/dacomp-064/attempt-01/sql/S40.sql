-- Check project categories
SELECT project_category_id, COUNT(*) n FROM jira__project_enhanced GROUP BY project_category_id ORDER BY n DESC