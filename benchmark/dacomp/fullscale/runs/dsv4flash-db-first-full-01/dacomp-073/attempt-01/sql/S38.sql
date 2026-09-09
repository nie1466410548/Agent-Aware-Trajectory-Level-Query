SELECT categories_department, COUNT(*) as active_postings
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department
ORDER BY categories_department