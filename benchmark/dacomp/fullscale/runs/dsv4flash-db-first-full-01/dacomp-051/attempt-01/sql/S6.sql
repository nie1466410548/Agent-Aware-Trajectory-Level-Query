SELECT team_id, COUNT(*) AS task_cnt, COUNT(DISTINCT assignee_user_id) AS users_cnt,
COUNT(*) FILTER (WHERE is_completed=1) AS completed_cnt FROM asana__task_lifecycle_analysis
GROUP BY team_id ORDER BY task_cnt DESC LIMIT 20