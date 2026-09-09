-- Get key accounts with their contact data for analysis
SELECT 
  a.account_id,
  a.account_name,
  a.industry_normalized,
  a.account_size_segment,
  a.company_size_category,
  a.annual_revenue,
  a.number_of_employees,
  a.total_contacts,
  a.geographic_region,
  a.churn_risk_level,
  a.customer_health_score,
  a.relationship_strength,
  a.total_opportunities,
  a.won_opportunities,
  a.current_pipeline_amount,
  a.total_won_amount,
  a.engagement_temperature,
  a.is_declining_engagement
FROM salesforce__customer_360_view a
WHERE a.annual_revenue >= 71234915
ORDER BY a.annual_revenue DESC