SELECT sample_repo_name, sample_path, content
FROM contents
WHERE sample_path ILIKE 'readme.md' OR sample_path ILIKE '%/readme.md';

