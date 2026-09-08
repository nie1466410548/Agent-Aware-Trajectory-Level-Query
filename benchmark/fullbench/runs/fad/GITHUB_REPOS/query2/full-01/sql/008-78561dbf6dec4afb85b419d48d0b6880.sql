SELECT id, COUNT(*) AS occurrences, COUNT(DISTINCT repo_name) AS repos
FROM files
WHERE path LIKE '%.swift'
GROUP BY id
ORDER BY occurrences DESC
LIMIT 10

