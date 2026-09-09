SELECT j.name, j.departments, j.hiring_managers, j.recruiters, j.sourcers
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY j.name