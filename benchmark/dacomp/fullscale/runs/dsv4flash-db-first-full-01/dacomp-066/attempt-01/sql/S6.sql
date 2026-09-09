SELECT DISTINCT j.name, j.departments, j.hiring_managers 
FROM greenhouse__job_enhanced j 
WHERE j.departments = 'Engineering' 
LIMIT 30