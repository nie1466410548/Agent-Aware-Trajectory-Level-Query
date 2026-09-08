SELECT COUNT(*) AS total_readme, COUNT(DISTINCT sample_repo_name) AS repos, COUNT(DISTINCT id) AS blobs FROM contents WHERE regexp_matches(lower(sample_path), '(^|/)readme\.md$')
