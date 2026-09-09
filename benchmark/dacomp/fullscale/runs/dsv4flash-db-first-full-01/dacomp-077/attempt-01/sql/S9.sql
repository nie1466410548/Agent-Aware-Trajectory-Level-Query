SELECT
  SUM(CASE WHEN predicted_clv_tier IS NULL THEN 1 ELSE 0 END) AS clv_tier_null,
  SUM(CASE WHEN predicted_ltv_tier IS NULL THEN 1 ELSE 0 END) AS ltv_tier_null,
  SUM(CASE WHEN rfm_composite_score IS NULL THEN 1 ELSE 0 END) AS rfm_null,
  SUM(CASE WHEN customer_value_tier IS NULL THEN 1 ELSE 0 END) AS cvtier_null,
  SUM(CASE WHEN is_valuable_user IS NULL THEN 1 ELSE 0 END) AS valuable_null,
  SUM(CASE WHEN comprehensive_customer_value IS NULL THEN 1 ELSE 0 END) AS ccv_null,
  SUM(CASE WHEN user_value_score IS NULL THEN 1 ELSE 0 END) AS uvs_null
FROM pendo__customer_lifecycle_insights