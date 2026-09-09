-- Get data for Python visualization: per-user metrics with segment
SELECT
  v.visitor_id,
  v.count_active_days,
  v.count_active_months,
  v.average_daily_minutes,
  v.average_daily_events,
  v.latest_nps_rating,
  v.sum_minutes,
  v.sum_events,
  v.first_event_on,
  v.last_event_on,
  a.avg_nps_rating AS account_avg_nps,
  COALESCE(fv.distinct_features, 0) AS distinct_features
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
LIMIT 8000