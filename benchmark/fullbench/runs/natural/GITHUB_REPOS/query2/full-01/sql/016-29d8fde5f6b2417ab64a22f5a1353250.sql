SELECT f.id, COUNT(*) AS occurrences_in_files,
       MIN(c.repo_data_description) AS description,
       MIN(c.sample_repo_name) AS sample_repo,
       MIN(c.sample_path) AS sample_path
FROM files f JOIN contents c ON f.id = c.id
WHERE f.id IN ('71a17ce92451858f3eb01aa8082551e48bc5550d','cc41f22d46f21f11c9e716b30cbaeb11f4ef80fc')
GROUP BY f.id;

