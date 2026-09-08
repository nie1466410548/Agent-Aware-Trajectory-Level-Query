SELECT regexp_extract(path, '\.([A-Za-z0-9]+)$', 1) AS ext, COUNT(*) AS n FROM files WHERE repo_name = 'torvalds/linux' GROUP BY ext ORDER BY n DESC LIMIT 15
