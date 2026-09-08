SELECT Project_Information
FROM project_info
WHERE coalesce(
    nullif(regexp_extract(Project_Information, 'stars? count of\s+([\d,]+)', 1), ''),
    nullif(regexp_extract(Project_Information, '([\d,]+)\s+stars?', 1), '')
) IS NULL

