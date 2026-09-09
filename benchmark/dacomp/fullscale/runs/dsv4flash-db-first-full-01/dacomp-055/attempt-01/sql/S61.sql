
SELECT investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
  total_sales_amount AS sales, digital_engagement_score AS digi_eng, nps_score AS nps,
  customer_health_score AS health, churn_probability AS churn
FROM customer360__customer_value_analysis
LIMIT 3000
