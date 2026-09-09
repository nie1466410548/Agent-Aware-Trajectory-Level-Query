SELECT
  'Quality Score' AS metric, MIN(quality_score) AS min_val, MAX(quality_score) AS max_val, ROUND(AVG(quality_score),2) AS avg_val, ROUND(AVG(CAST(quality_score AS REAL)),2) AS avg_real FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Financial Health Score', MIN(financial_health_score), MAX(financial_health_score), ROUND(AVG(financial_health_score),2), ROUND(AVG(CAST(financial_health_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Innovation Capability Score', MIN(innovation_capability_score), MAX(innovation_capability_score), ROUND(AVG(innovation_capability_score),2), ROUND(AVG(CAST(innovation_capability_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Cybersecurity Score', MIN(cybersecurity_score), MAX(cybersecurity_score), ROUND(AVG(cybersecurity_score),2), ROUND(AVG(CAST(cybersecurity_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Market Volatility Index', MIN(market_volatility_index), MAX(market_volatility_index), ROUND(AVG(market_volatility_index),4), ROUND(AVG(CAST(market_volatility_index AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Alternative Suppliers Count', MIN(alternative_suppliers_count), MAX(alternative_suppliers_count), ROUND(AVG(alternative_suppliers_count),2), ROUND(AVG(CAST(alternative_suppliers_count AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Price Volatility Coefficient', MIN(price_volatility_coefficient), MAX(price_volatility_coefficient), ROUND(AVG(price_volatility_coefficient),4), ROUND(AVG(CAST(price_volatility_coefficient AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Avg Payment Delay', MIN(avg_payment_delay), MAX(avg_payment_delay), ROUND(AVG(avg_payment_delay),2), ROUND(AVG(CAST(avg_payment_delay AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Overdue Payment %', MIN(overdue_payment_percentage), MAX(overdue_payment_percentage), ROUND(AVG(overdue_payment_percentage),2), ROUND(AVG(CAST(overdue_payment_percentage AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Spend Concentration Ratio', MIN(spend_concentration_ratio), MAX(spend_concentration_ratio), ROUND(AVG(spend_concentration_ratio),4), ROUND(AVG(CAST(spend_concentration_ratio AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Total Vendor Spend', MIN(total_vendor_spend), MAX(total_vendor_spend), ROUND(AVG(total_vendor_spend),2), ROUND(AVG(CAST(total_vendor_spend AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Switching Cost Estimate', MIN(switching_cost_estimate), MAX(switching_cost_estimate), ROUND(AVG(switching_cost_estimate),2), ROUND(AVG(CAST(switching_cost_estimate AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Vendor Relationship Days', MIN(vendor_relationship_days), MAX(vendor_relationship_days), ROUND(AVG(vendor_relationship_days),2), ROUND(AVG(CAST(vendor_relationship_days AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Days Since Last Transaction', MIN(days_since_last_transaction), MAX(days_since_last_transaction), ROUND(AVG(days_since_last_transaction),2), ROUND(AVG(CAST(days_since_last_transaction AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Total Transactions', MIN(total_transactions), MAX(total_transactions), ROUND(AVG(total_transactions),2), ROUND(AVG(CAST(total_transactions AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')