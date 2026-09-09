-- Compute ALL features with avg CCV for users and non-users
WITH tracked AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
base_clv AS (
  SELECT c.visitor_id, c.comprehensive_customer_value
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked t ON c.visitor_id = t.visitor_id
)
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_users,
  AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_nonusers,
  (SELECT COUNT(*) FROM base_clv) AS n_tracked_total
FROM pendo__feature f
CROSS JOIN base_clv bc
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id
GROUP BY f.feature_id
ORDER BY (AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) - AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)) DESC
LIMIT 60