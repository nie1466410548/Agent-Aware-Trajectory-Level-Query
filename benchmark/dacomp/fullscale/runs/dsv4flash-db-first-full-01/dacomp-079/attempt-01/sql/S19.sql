-- Top features used by single-feature-heavy users
SELECT
  f.feature_id,
  f.feature_name,
  f.product_area_name,
  f.page_name,
  f.app_display_name,
  f.app_platform,
  COUNT(DISTINCT vf.visitor_id) AS n_single_feature_users,
  SUM(vf.sum_clicks) AS total_clicks,
  ROUND(AVG(vf.sum_clicks), 2) AS avg_clicks_per_user
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
GROUP BY f.feature_id
ORDER BY n_single_feature_users DESC
LIMIT 20