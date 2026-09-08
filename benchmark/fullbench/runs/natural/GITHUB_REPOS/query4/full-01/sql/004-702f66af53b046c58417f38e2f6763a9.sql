SELECT repo_name, COUNT(*) AS commit_count FROM commits GROUP BY repo_name ORDER BY commit_count DESC LIMIT 15
