SELECT id, sample_repo_name, sample_ref, sample_path,
       CAST(regexp_extract(repo_data_description, '(\d+) times', 1) AS INTEGER) AS copies,
       repo_data_description
FROM contents
WHERE sample_path LIKE '%.swift'
  AND lower(repo_data_description) LIKE '%non-binary%'
ORDER BY copies DESC
LIMIT 30;
