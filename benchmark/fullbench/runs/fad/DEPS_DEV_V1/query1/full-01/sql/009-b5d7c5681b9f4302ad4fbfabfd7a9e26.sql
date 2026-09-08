SELECT Project_Information,
       regexp_extract(Project_Information, 'The project ([^ ]+)', 1) AS project,
       TRY_CAST(regexp_extract(Project_Information, '(\d+) stars?', 1) AS BIGINT) AS stars
FROM project_info

