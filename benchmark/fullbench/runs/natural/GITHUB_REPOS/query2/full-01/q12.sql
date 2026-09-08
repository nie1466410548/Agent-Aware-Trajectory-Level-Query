SELECT
  (SELECT COUNT(*) FROM files WHERE path LIKE '%.swift') AS swift_files,
  (SELECT COUNT(*) FROM files f JOIN contents c ON f.id = c.id) AS joined_any,
  (SELECT COUNT(*) FROM files f JOIN contents c ON f.id = c.id WHERE f.path LIKE '%.swift') AS joined_swift,
  (SELECT COUNT(*) FROM files f JOIN contents c ON f.id = c.id WHERE f.path LIKE '%.swift' AND lower(c.repo_data_description) LIKE '%non-binary%') AS joined_swift_nonbin;
