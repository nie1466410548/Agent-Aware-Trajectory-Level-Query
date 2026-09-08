SELECT id, COUNT(*) AS copies, COUNT(DISTINCT repo_name) AS repos, MIN(path) AS sample_path, MIN(repo_name) AS sample_repo
FROM files
WHERE path LIKE '%.swift'
GROUP BY id
ORDER BY copies DESC
LIMIT 20;

