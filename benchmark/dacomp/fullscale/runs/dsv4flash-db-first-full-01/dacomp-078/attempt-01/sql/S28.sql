SELECT a.account_id, a.count_associated_visitors, COUNT(DISTINCT v.visitor_id) AS actual_visitors
FROM pendo__account a JOIN pendo__visitor v ON a.account_id = v.account_id
GROUP BY a.account_id
ORDER BY a.count_associated_visitors - COUNT(DISTINCT v.visitor_id) DESC
LIMIT 10