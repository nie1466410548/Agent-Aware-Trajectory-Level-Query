SELECT r.requisition_code, r.team, r.status, p.categories_department, p.posting_title
FROM lever__requisition_enhanced r
JOIN lever__posting_enhanced p ON r.requisition_code = p.requisition_code
LIMIT 20