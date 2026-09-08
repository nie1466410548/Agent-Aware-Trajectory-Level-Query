SELECT f.id,
       MAX(CAST(regexp_extract(c.repo_data_description, '(\d+) times', 1) AS INTEGER)) AS copies,
       STRING_AGG(DISTINCT f.repo_name, ' | ') AS repos,
       MIN(f.path) AS path,
       MIN(c.sample_path) AS sample_path
FROM files f
JOIN contents c ON f.id = c.id
WHERE f.path LIKE '%.swift'
  AND lower(c.repo_data_description) LIKE '%non-binary%'
GROUP BY f.id
ORDER BY copies DESC
LIMIT 100;

