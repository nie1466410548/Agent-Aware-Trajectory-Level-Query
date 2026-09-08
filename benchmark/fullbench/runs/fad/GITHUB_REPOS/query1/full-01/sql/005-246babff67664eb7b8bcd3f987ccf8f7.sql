SELECT CASE WHEN path LIKE '%/%' THEN 'nested' ELSE 'root' END AS location, COUNT(*) FROM files WHERE regexp_matches(lower(path), '(^|/)readme\.md$') GROUP BY 1
