SELECT status,
       SUM(headcount_total) as total_headcount,
       SUM(headcount_hired) as total_hired,
       SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) as infinite_cnt,
       COUNT(*) as cnt
FROM lever__requisition_enhanced
GROUP BY status