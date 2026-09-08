SELECT COUNT(*) AS total_files, COUNT(*) FILTER (WHERE path LIKE '%.swift') AS swift_files FROM files;
