SELECT COUNT(*) AS total_rows, COUNT(DISTINCT repo_name) AS distinct_repos,
SUM(CASE WHEN language_description LIKE '%Python%' THEN 1 ELSE 0 END) AS python_repos
FROM languages;

