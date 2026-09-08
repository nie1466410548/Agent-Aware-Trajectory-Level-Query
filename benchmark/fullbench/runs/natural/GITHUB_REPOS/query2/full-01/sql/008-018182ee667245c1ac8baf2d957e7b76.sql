SELECT id, COUNT(*) AS file_rows, COUNT(DISTINCT repo_name) AS n_repos
FROM files
WHERE id = '6f4cdb70f044b0486a24a07403600cb964a02672'
GROUP BY id;

