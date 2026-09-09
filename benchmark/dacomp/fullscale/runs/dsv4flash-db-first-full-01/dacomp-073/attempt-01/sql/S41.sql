SELECT r.requisition_code, r.team, r.status, r.headcount_total, r.headcount_hired, r.headcount_infinite
FROM lever__requisition_enhanced r
WHERE r.has_posting = 1
LIMIT 20