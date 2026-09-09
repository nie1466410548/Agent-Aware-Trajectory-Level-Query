SELECT
  SUM(CASE WHEN vendor_name LIKE 'Vendor_%' THEN 1 ELSE 0 END) AS synthetic_named,
  SUM(CASE WHEN vendor_category_name = 'General Supplier' THEN 1 ELSE 0 END) AS general_supplier_count,
  SUM(CASE WHEN total_vendor_spend < 1000 THEN 1 ELSE 0 END) AS tiny_spend,
  SUM(CASE WHEN spend_concentration_ratio = 1.0 THEN 1 ELSE 0 END) AS conc_100pct
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')