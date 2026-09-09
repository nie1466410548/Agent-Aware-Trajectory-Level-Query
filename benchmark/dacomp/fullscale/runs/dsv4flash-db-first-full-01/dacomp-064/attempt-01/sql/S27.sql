-- Distinct assignee_user_id per assignee_name sample
SELECT assignee_name, COUNT(DISTINCT assignee_user_id) AS n_ids, COUNT(*) AS n_issues
FROM jira__issue_enhanced
GROUP BY assignee_name
HAVING n_ids > 1
LIMIT 10