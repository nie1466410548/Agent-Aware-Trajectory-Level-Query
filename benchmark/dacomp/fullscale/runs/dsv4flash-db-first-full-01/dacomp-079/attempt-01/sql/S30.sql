-- Fair comparison within the >60 active-day population
SELECT
  CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END AS segment,
  COUNT(*) AS n_users,
  ROUND(AVG(v.count_active_days), 1) AS avg_active_days,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(julianday(v.last_event_on) - julianday(v.first_event_on)), 1) AS avg_span_days,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_minutes,
  ROUND(AVG(v.average_daily_events), 2) AS avg_daily_events,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(AVG(a.avg_nps_rating), 3) AS avg_account_nps
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
WHERE v.count_active_days > 60
GROUP BY segment