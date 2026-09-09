SELECT a.account_id,
  COUNT(DISTINCT v.visitor_id) AS visitors_in_account,
  SUM(CASE WHEN dm.visitor_id IS NOT NULL THEN 1 ELSE 0 END) AS visitors_with_metrics
FROM pendo__account a
LEFT JOIN pendo__visitor v ON a.account_id = v.account_id
LEFT JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_daily_metrics) dm ON v.visitor_id = dm.visitor_id
GROUP BY a.account_id
LIMIT 10