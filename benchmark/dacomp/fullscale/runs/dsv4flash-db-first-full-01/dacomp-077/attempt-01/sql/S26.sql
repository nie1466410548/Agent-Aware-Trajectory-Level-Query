WITH tracked_visitors AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
base AS (
  SELECT AVG(c.comprehensive_customer_value) AS avg_ccv_overall,
         COUNT(*) AS n_tracked
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked_visitors tv ON c.visitor_id = tv.visitor_id
)
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(c.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT avg_ccv_overall FROM base) AS avg_ccv_overall,
  (SELECT n_tracked FROM base) AS n_tracked
FROM pendo__feature f
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
LEFT JOIN pendo__customer_lifecycle_insights c ON vf.visitor_id = c.visitor_id
GROUP BY f.feature_id
ORDER BY (AVG(c.comprehensive_customer_value) - (SELECT avg_ccv_overall FROM base)) DESC
LIMIT 60