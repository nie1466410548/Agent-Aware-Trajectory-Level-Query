SELECT posting_hiring_manager_name, COUNT(DISTINCT categories_department) as dept_cnt, COUNT(*) as posting_cnt
FROM lever__posting_enhanced
GROUP BY posting_hiring_manager_name
HAVING dept_cnt > 1
ORDER BY posting_cnt DESC
LIMIT 15