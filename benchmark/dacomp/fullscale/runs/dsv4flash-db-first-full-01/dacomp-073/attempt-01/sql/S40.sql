SELECT p.categories_department, r.status, COUNT(DISTINCT r.requisition_id) as cnt
FROM lever__requisition_enhanced r
LEFT JOIN lever__posting_enhanced p ON p.requisition_code = r.requisition_code
GROUP BY p.categories_department, r.status
ORDER BY p.categories_department, r.status