-- App/platform breakdown: which app do single-feature users primarily use?
SELECT
  f.app_display_name,
  f.app_platform,
  COUNT(DISTINCT vf.visitor_id) AS n_single_feature_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
  AND f.app_display_name IS NOT NULL
GROUP BY f.app_display_name, f.app_platform
ORDER BY n_single_feature_users DESC
LIMIT 15