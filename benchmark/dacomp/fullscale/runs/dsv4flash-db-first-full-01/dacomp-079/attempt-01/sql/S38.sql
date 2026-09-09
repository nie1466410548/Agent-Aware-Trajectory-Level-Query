-- Final check: is there a correlation between distinct features and daily minutes for the heavy users?
-- This helps understand the "dose-response" relationship
SELECT
  fv.distinct_features,
  COUNT(*) AS n_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(AVG(v.count_active_days), 1) AS avg_active_days,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60
GROUP BY fv.distinct_features
ORDER BY fv.distinct_features