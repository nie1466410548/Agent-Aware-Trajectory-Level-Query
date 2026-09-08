WITH pi AS (
  SELECT regexp_extract(Project_Information, 'The project ([^ ]+)', 1) AS project,
         TRY_CAST(regexp_extract(Project_Information, '(\d+) stars', 1) AS BIGINT) AS stars
  FROM project_info
)
SELECT ppv.Name, ppv.Version, pi.project, pi.stars
FROM project_packageversion ppv
JOIN pi ON ppv.ProjectName = pi.project
WHERE ppv.System = 'NPM' AND ppv.ProjectType = 'GITHUB'
GROUP BY ppv.Name, ppv.Version, pi.project, pi.stars
