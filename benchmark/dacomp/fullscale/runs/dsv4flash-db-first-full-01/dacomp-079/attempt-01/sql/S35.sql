-- Feature concentration data for Python
WITH single_feature_users AS (
  SELECT v.visitor_id
  FROM pendo__visitor v
  JOIN (SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
        FROM pendo__visitor_feature GROUP BY visitor_id) fv ON fv.visitor_id = v.visitor_id
  WHERE v.count_active_days > 60 AND fv.distinct_features < 5
)
SELECT
  vf.visitor_id,
  vf.feature_id,
  f.feature_name,
  f.product_area_name,
  f.page_name,
  f.app_display_name,
  vf.sum_clicks,
  vf.sum_minutes,
  vf.avg_daily_minutes,
  vf.count_click_events
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
WHERE vf.visitor_id IN (SELECT visitor_id FROM single_feature_users)
ORDER BY vf.visitor_id, vf.sum_clicks DESC