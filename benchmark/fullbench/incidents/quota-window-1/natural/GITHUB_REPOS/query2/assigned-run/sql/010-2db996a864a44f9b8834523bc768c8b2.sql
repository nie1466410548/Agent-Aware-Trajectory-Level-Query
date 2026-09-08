SELECT id, COUNT(*) AS copies_in_files, COUNT(DISTINCT repo_name) AS repos, MIN(repo_name) AS r, MIN(path) AS p
FROM files
WHERE id IN ('6f4cdb70f044b0486a24a07403600cb964a02672','a34c3d906831a12ffffa1b5d0fc30505126e9b69','c4d6ced29fbff41f82c1e9ebd9d4e5fe0c4fd795')
GROUP BY id;

