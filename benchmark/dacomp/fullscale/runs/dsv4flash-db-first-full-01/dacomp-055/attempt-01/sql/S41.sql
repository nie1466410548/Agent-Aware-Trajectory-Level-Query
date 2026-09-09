SELECT COUNT(*) AS cnt
FROM (SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate, 
       v.support_resolution_efficiency, v.customer_lifetime_value, v.acquisition_cost,
       v.lifecycle_stage, v.industry_vertical, v.company_size_tier, 
       v.customer_onboarding_score, v.team_size, v.decision_maker_level
      FROM customer360__customer_value_analysis v
      WHERE v.primary_email IS NOT NULL) v