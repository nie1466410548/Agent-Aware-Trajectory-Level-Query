SELECT id, COUNT(*) AS total_copies,
       COUNT(*) FILTER (WHERE path LIKE '%.swift') AS swift_copies,
       COUNT(DISTINCT repo_name) AS n_repos,
       MIN(path) AS sample_path
FROM files
WHERE id IN (SELECT DISTINCT id FROM files WHERE path LIKE '%.swift')
GROUP BY id
ORDER BY total_copies DESC, id
LIMIT 10;
