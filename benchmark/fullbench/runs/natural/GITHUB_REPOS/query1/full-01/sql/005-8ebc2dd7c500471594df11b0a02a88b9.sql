SELECT COUNT(*) AS total_readme_files,
COUNT(DISTINCT sample_repo_name) AS repos_with_readme
FROM contents
WHERE sample_path ILIKE '%readme.md%';

