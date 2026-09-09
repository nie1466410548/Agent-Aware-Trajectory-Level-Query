SELECT status, headcount_total, headcount_hired, headcount_infinite
FROM lever__requisition_enhanced
WHERE status = 'open'
LIMIT 20