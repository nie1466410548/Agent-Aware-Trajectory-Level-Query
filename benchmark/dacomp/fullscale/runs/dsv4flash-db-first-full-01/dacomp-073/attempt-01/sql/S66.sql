-- Get the most common department for each hiring manager
SELECT pm.hiring_manager_name, pm.categories_department, pm.cnt as dept_posting_cnt
FROM (
  SELECT posting_hiring_manager_name as hiring_manager_name, categories_department, COUNT(*) as cnt,
         ROW_NUMBER() OVER (PARTITION BY posting_hiring_manager_name ORDER BY COUNT(*) DESC) as rn
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name, categories_department
) pm
WHERE pm.rn = 1
ORDER BY pm.hiring_manager_name
LIMIT 20