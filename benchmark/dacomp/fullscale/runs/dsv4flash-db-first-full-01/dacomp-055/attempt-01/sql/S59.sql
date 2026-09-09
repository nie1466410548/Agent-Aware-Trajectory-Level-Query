
SELECT investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier
FROM customer360__customer_value_analysis
LIMIT 2000
