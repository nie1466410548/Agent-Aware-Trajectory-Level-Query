-- Check whether any binary .swift file outranks, and confirm the top file's details/content
SELECT
  id,
  MAX(CAST(regexp_extract(repo_data_description, '(\d+) times', 1) AS INTEGER)) AS copies,
  MAX(CASE WHEN LOWER(repo_data_description) LIKE '%non-binary%' THEN 0 ELSE 1 END) AS is_binary,
  ANY_VALUE(sample_repo_name) AS sample_repo_name,
  ANY_VALUE(sample_path) AS sample_path
FROM contents
WHERE sample_path LIKE '%.swift'
GROUP BY id
ORDER BY copies DESC
LIMIT 5

