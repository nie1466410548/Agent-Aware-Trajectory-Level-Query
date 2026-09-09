SELECT categories_department,
       COUNT(DISTINCT posting_hiring_manager_name) as all_hms,
       COUNT(*) as all_postings
FROM lever__posting_enhanced
GROUP BY categories_department
ORDER BY categories_department