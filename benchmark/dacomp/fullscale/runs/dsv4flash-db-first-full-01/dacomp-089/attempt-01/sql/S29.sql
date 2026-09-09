SELECT a.account_id, a.account_name, a.industry_normalized, a.account_size_segment, a.company_size_category, a.annual_revenue, a.number_of_employees, a.total_contacts, a.geographic_region, a.churn_risk_level, a.customer_health_score, a.relationship_strength
FROM salesforce__customer_360_view a
WHERE a.annual_revenue >= 71234915
ORDER BY a.annual_revenue DESC