SELECT COUNT(DISTINCT account_id) AS accts_with_metrics
FROM pendo__visitor v
JOIN pendo__visitor_daily_metrics dm ON v.visitor_id = dm.visitor_id