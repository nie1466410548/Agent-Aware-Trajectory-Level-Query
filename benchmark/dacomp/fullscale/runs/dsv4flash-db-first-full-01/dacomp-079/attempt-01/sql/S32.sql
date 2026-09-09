-- For single-feature users, what's the distribution of their main feature's product area?
SELECT
  f.product_area_name,
  f.feature_name,
  COUNT(DISTINCT vf.visitor_id) AS n_users,
  SUM(vf.sum_clicks) AS total_clicks,
  ROUND(AVG(vf.avg_daily_minutes), 2) AS avg_daily_minutes_in_feature,
  ROUND(AVG(vf.count_click_events), 1) AS avg_click_events
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
GROUP BY f.product_area_name, f.feature_name
ORDER BY n_users DESC
LIMIT 20