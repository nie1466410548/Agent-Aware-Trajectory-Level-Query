SELECT vendor_id, vendor_name, vendor_category_name, total_vendor_spend, spend_concentration_ratio, strategic_importance_level, dependency_level, activity_status, days_since_last_transaction, contract_expiry_date, risk_level, vendor_risk_score
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend ASC
LIMIT 15