SELECT date_day, date_week, status, issue_type, COUNT(*) n
FROM jira__daily_issue_field_history
GROUP BY date_day, date_week, status, issue_type
ORDER BY date_day
LIMIT 10