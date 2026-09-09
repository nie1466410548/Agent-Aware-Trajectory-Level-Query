SELECT categories_department, state, COUNT(*) as cnt
FROM lever__posting_enhanced
WHERE categories_department = 'Marketing'
GROUP BY categories_department, state