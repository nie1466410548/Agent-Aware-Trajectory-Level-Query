-- Browser and OS breakdown for single-feature vs normal users
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  v.last_browser_name,
  v.last_operating_system,
  COUNT(*) AS n_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment, v.last_browser_name, v.last_operating_system
ORDER BY segment, n_users DESC
LIMIT 20