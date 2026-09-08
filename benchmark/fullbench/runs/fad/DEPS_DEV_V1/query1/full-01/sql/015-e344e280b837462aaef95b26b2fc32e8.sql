WITH pi AS (
  SELECT
    lower(nullif(regexp_extract(Project_Information, '([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', 1), '')) AS project,
    TRY_CAST(replace(coalesce(
        nullif(regexp_extract(Project_Information, 'stars? count of\s+([\d,]+)', 1), ''),
        nullif(regexp_extract(Project_Information, '([\d,]+)\s+stars?', 1), ''),
        nullif(regexp_extract(Project_Information, 'starred by\s+([\d,]+)', 1), '')
    ), ',', '') AS BIGINT) AS stars
  FROM project_info
),
pi2 AS (
  SELECT project, max(stars) AS stars FROM pi WHERE project IS NOT NULL GROUP BY project
)
SELECT ppv.Name, ppv.Version, pi2.project, pi2.stars
FROM project_packageversion ppv
JOIN pi2 ON lower(ppv.ProjectName) = pi2.project
WHERE ppv.System = 'NPM' AND ppv.ProjectType = 'GITHUB'
GROUP BY ppv.Name, ppv.Version, pi2.project, pi2.stars

