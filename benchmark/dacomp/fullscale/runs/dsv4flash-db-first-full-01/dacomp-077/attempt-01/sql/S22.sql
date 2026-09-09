SELECT
  f.feature_id, f.feature_name, f.count_visitors,
  AVG(c.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT AVG(c2.comprehensive_customer_value) FROM pendo__customer_lifecycle_insights c2 WHERE c2.visitor_id IN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AND c2.visitor_id NOT IN (SELECT visitor_id FROM pendo__visitor_feature vf2 WHERE vf2.feature_id = f.feature_id)) AS avg_ccv_nonusers,
  COUNT(DISTINCT vf.visitor_id) AS n_users_in_vf
FROM pendo__feature f
JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
JOIN pendo__customer_lifecycle_insights c ON vf.visitor_id = c.visitor_id
GROUP BY f.feature_id
HAVING f.count_visitors < 200
ORDER BY (avg_ccv_users - avg_ccv_nonusers) DESC
LIMIT 20