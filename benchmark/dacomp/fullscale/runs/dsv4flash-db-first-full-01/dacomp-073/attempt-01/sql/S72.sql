SELECT categories_department,
       COUNT(*) as total_postings,
       COUNT(DISTINCT posting_hiring_manager_name) as distinct_hms,
       ROUND(1.0*COUNT(*) / COUNT(DISTINCT posting_hiring_manager_name), 2) as postings_per_hm
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department
ORDER BY categories_department