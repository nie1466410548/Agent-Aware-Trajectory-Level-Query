SELECT f.id, f.repo_name, f.path, f.mode, c.repo_data_description, c.sample_repo_name, c.sample_path
FROM files f LEFT JOIN contents c ON c.id = f.id
WHERE f.id = 'a6fb31fa1e4b1647e8862580703add8c6205c6d1';
