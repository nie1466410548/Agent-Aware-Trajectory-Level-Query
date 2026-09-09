
SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
  investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
  digital_engagement_score AS digi_eng, nps_score AS nps,
  customer_health_score AS health, churn_probability AS churn,
  competitive_pressure_index AS cpi, renewal_probability AS renew,
  expansion_revenue_potential AS expansion, time_to_value_days AS ttv
FROM customer360__customer_value_analysis
LIMIT 5
