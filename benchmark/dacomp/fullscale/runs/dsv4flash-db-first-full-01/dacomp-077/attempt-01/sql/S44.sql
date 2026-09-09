SELECT
  COUNT(*) AS n,
  AVG(comprehensive_customer_value) AS avg_ccv,
  MIN(comprehensive_customer_value) AS min_ccv,
  MAX(comprehensive_customer_value) AS max_ccv,
  AVG(user_value_score) AS avg_uvs,
  MIN(user_value_score) AS min_uvs,
  MAX(user_value_score) AS max_uvs,
  SUM(CASE WHEN comprehensive_customer_value >= 500 THEN 1 ELSE 0 END) AS n_high_value
FROM pendo__customer_lifecycle_insights