SELECT
  id,
  MAX(CAST(regexp_extract(repo_data_description, '(\d+) times', 1) AS INTEGER)) AS copies,
  ANY_VALUE(sample_repo_name) AS sample_repo_name,
  ANY_VALUE(sample_path) AS sample_path,
  COUNT(*) AS rows_in_contents
FROM contents
WHERE sample_path LIKE '%.swift'
  AND LOWER(repo_data_description) LIKE '%non-binary%'
GROUP BY id
ORDER BY copies DESC
LIMIT 30

