SELECT COUNT(*) as single_dept_hms
FROM (
  SELECT posting_hiring_manager_name
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name
  HAVING COUNT(DISTINCT categories_department) = 1
)