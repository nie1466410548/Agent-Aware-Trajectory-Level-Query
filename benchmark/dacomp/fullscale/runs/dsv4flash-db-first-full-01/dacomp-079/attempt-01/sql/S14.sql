SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  COUNT(*) AS n_users,
  ROUND(AVG(v.latest_nps_rating), 4) AS avg_nps,
  ROUND(AVG(v.average_daily_minutes), 4) AS avg_daily_minutes,
  ROUND(AVG(v.average_daily_events), 4) AS avg_daily_events,
  ROUND(AVG(v.count_active_days), 2) AS avg_active_days,
  ROUND(AVG(fv.distinct_features), 2) AS avg_distinct_features
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment