SELECT
  MIN(comprehensive_customer_value) AS min_ccv,
  MAX(comprehensive_customer_value) AS max_ccv,
  AVG(comprehensive_customer_value) AS avg_ccv,
  MIN(user_value_score) AS min_uvs,
  MAX(user_value_score) AS max_uvs,
  AVG(user_value_score) AS avg_uvs,
  COUNT(*) AS n,
  COUNT(DISTINCT predicted_clv_tier) AS n_tiers
FROM pendo__customer_lifecycle_insights