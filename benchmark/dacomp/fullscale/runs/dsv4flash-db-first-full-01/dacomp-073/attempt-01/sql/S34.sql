SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department, substr(created_at, 1, 7)
ORDER BY categories_department, ym