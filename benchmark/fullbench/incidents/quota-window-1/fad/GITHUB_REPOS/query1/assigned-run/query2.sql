SELECT sample_path, COUNT(*) AS n
FROM contents
WHERE lower(sample_path) LIKE '%readme%'
GROUP BY sample_path
ORDER BY n DESC
LIMIT 30;
