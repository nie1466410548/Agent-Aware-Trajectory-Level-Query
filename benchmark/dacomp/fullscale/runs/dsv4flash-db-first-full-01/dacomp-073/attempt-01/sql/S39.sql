SELECT r.status, COUNT(*) as cnt
FROM lever__requisition_enhanced r
GROUP BY r.status
ORDER BY r.status