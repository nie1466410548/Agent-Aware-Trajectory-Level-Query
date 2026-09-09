SELECT headcount_total, headcount_hired, headcount_infinite, COUNT(*) as cnt
FROM lever__requisition_enhanced
WHERE status = 'open'
GROUP BY headcount_total, headcount_hired, headcount_infinite
ORDER BY cnt DESC