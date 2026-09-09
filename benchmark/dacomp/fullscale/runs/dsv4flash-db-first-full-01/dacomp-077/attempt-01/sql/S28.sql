SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  f.count_accounts,
  f.sum_clicks,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_users,
  AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_nonusers,
  COUNT(CASE WHEN vf.visitor_id IS NOT NULL THEN 1 END) AS n_user_obs,
  COUNT(CASE WHEN vf.visitor_id IS NULL THEN 1 END) AS n_nonuser_obs
FROM pendo__feature f
CROSS JOIN (
  SELECT c.visitor_id, c.comprehensive_customer_value
  FROM pendo__customer_lifecycle_insights c
  JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id
) bc
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id
GROUP BY f.feature_id
ORDER BY f.feature_id