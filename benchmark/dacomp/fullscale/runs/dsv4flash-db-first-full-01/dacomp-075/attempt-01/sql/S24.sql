SELECT
  vendor_id, vendor_name, vendor_category_name, geographic_region,
  total_vendor_spend, spend_concentration_ratio, strategic_importance_level,
  -- Financial Resilience Metrics
  avg_payment_delay, overdue_payment_percentage, overdue_invoices, total_payable_invoices, financial_health_score,
  -- Operational Resilience Metrics
  quality_score, cybersecurity_score, innovation_capability_score,
  -- Market Resilience
  market_volatility_index, alternative_suppliers_count, price_volatility_coefficient,
  -- Strategic Resilience
  geographic_region, contract_expiry_date, environmental_rating, vendor_relationship_days, days_since_last_transaction,
  -- Additional
  dependency_level, relationship_stability, activity_status, risk_level, vendor_risk_score, supplier_tier, management_priority,
  switching_cost_estimate, total_payables, total_expenses, total_transactions, active_months
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend DESC