SELECT p.requisition_code, p.categories_department, r.team, r.status, r.headcount_total, r.headcount_hired, r.headcount_infinite
FROM lever__posting_enhanced p
JOIN lever__requisition_enhanced r ON p.requisition_code = r.requisition_code
LIMIT 15