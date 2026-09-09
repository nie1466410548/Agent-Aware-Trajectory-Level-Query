SELECT a.account_id, a.count_associated_visitors, a.count_active_days, a.count_active_months,
       a.sum_minutes, a.sum_events, a.avg_nps_rating, a.last_event_on
FROM pendo__account a
WHERE a.account_id IN (
  SELECT DISTINCT v.account_id
  FROM pendo__visitor v
  JOIN pendo__visitor_daily_metrics dm ON v.visitor_id = dm.visitor_id
)
ORDER BY a.account_id