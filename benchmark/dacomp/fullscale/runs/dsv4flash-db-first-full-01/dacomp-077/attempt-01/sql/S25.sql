-- Compute for each feature: avg CCV of users vs non-users, and usage stats
WITH tracked_visitors AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
feature_usage AS (
  SELECT
    f.feature_id,
    f.feature_name,
    f.count_visitors AS total_visitors,
    f.product_area_name,
    f.is_core_event,
    f.page_name
  FROM pendo__feature f
),
user_clv AS (
  SELECT
    c.visitor_id,
    c.comprehensive_customer_value,
    c.user_value_score,
    c.feature_adoption_rate,
    c.lifecycle_stage,
    c.overall_health_score
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked_visitors tv ON c.visitor_id = tv.visitor_id
),
feature_impact AS (
  SELECT
    fu.feature_id,
    fu.feature_name,
    fu.total_visitors,
    fu.product_area_name,
    fu.is_core_event,
    fu.page_name,
    vf.visitor_id
  FROM feature_usage fu
  LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = fu.feature_id
)
SELECT
  fi.feature_id,
  fi.feature_name,
  fi.total_visitors,
  fi.product_area_name,
  fi.is_core_event,
  fi.page_name,
  COUNT(DISTINCT fi.visitor_id) AS n_tracked_users,
  AVG(uc.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT AVG(uc2.comprehensive_customer_value) FROM user_clv uc2
   WHERE uc2.visitor_id NOT IN (SELECT vf2.visitor_id FROM pendo__visitor_feature vf2 WHERE vf2.feature_id = fi.feature_id)
  ) AS avg_ccv_nonusers,
  (SELECT COUNT(*) FROM user_clv) AS n_tracked_total
FROM feature_impact fi
LEFT JOIN user_clv uc ON fi.visitor_id = uc.visitor_id
GROUP BY fi.feature_id
ORDER BY (avg_ccv_users - avg_ccv_nonusers) DESC
LIMIT 50