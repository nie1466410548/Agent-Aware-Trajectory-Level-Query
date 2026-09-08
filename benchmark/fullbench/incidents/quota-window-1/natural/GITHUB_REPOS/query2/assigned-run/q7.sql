SELECT id, sample_repo_name, sample_path, repo_data_description
FROM contents
WHERE sample_path LIKE '%.swift' AND lower(repo_data_description) LIKE '%non-binary%'
ORDER BY CAST(regexp_extract(repo_data_description, '(\d+) times', 1) AS INTEGER) DESC
LIMIT 10;
