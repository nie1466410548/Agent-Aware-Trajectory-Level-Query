SELECT COUNT(DISTINCT issue_id) AS n_issues, COUNT(DISTINCT date_day) AS n_days, COUNT(DISTINCT assignee) AS n_assignees, COUNT(DISTINCT reporter) AS n_reporters
FROM jira__daily_issue_field_history