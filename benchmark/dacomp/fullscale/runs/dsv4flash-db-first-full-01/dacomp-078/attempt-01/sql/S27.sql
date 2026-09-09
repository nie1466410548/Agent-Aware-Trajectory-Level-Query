SELECT a.account_id, COUNT(DISTINCT v.visitor_id) AS actual_visitors
FROM pendo__account a LEFT JOIN pendo__visitor v ON a.account_id = v.account_id
GROUP BY a.account_id
HAVING COUNT(DISTINCT v.visitor_id) < a.count_associated_visitors
LIMIT 5