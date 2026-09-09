SELECT
  AVG(comprehensive_customer_value) AS avg_ccv_all,
  MIN(comprehensive_customer_value) AS min_ccv_all,
  MAX(comprehensive_customer_value) AS max_ccv_all,
  (SELECT AVG(c2.comprehensive_customer_value) FROM pendo__customer_lifecycle_insights c2 JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) vf2 ON c2.visitor_id = vf2.visitor_id) AS avg_ccv_tracked
FROM pendo__customer_lifecycle_insights